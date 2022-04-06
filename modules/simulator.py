# Friedjof Noweck
# 2021-12-08 Mi
from typing import Tuple
from tkinter import *
import numpy as np

from modules.arm import Segment, Arm, Pentagon
from modules.vectors import Vector

from threading import Thread
import time


class Simulator:
    def __init__(self, arms: Tuple[Arm, Arm], configuration: dict, ui: bool = True):
        self.arms = arms
        self.configs = configuration
        self.origin: Tuple[int, int] = self.configs["origin"]
        self.ui = ui

        self.cached_pentagon: Pentagon = self.angles(135.0, 135.0)

        if self.ui:
            self.items: dict = {}

            self.win = Tk()
            self.win.geometry(
                f"{self.configs['geometry']['width']}x"
                f"{self.configs['geometry']['height'] + 100}+"
                f"{self.configs['win pos']}")
            self.win.configure(bg=self.configs['bg'])
            self.win.title(self.configs["title"])

            self.canvas = Canvas(self.win, **self.configs['geometry'])
            self.canvas.config(bg=self.configs['bg'])
            self.canvas.pack()

            self.canvas.bind("<B1-Motion>", self._update_position)

            self.de_angle = IntVar(self.canvas)
            self.de = Scale(
                self.win, from_=0, to=360, bg="red",
                length=self.configs['geometry']['width'], orient=HORIZONTAL,
                command=self._update_degree, variable=self.de_angle
            )
            self.de_angle.set(90)
            self.de.pack()

            self.ga_angle = IntVar(self.canvas)
            self.ga = Scale(
                self.win, from_=0, to=360, bg="blue",
                length=self.configs['geometry']['width'], orient=HORIZONTAL,
                command=self._update_degree, variable=self.ga_angle
            )
            self.ga_angle.set(90)
            self.ga.pack()

            self.__grid()
            self.__display_motors()

    def _update_position(self, event):
        p: Pentagon = self.position(
            Vector(*self._relative_coord(event.x, event.y))
        )

        if not self.pentagon_is_invalid(p):
            self.update(p)

    def _update_degree(self, event):
        p: Pentagon = self.angles(
            self.de_angle.get(), self.ga_angle.get()
        )

        if not self.pentagon_is_invalid(p):
            self.update(p)

    def __grid(self, color: str = "#555", line_width: int = 1, fineness: int = 15) -> None:
        for i in range(0, self.configs['geometry']['height'], fineness):
            self.canvas.create_line(
                0, i, self.configs['geometry']['width'], i,
                fill=color, width=line_width
            )
        for i in range(0, self.configs['geometry']['width'], fineness):
            self.canvas.create_line(
                i, 0, i, self.configs['geometry']['height'],
                fill=color, width=line_width
            )

    def __display_motors(self, size: int = 20, fill: str = "#ABC") -> None:
        for a in self.arms:
            self.canvas.create_rectangle(
                *self._absolut_coord(x=a.axis_pos[0] - size, y=a.axis_pos[1] - size),
                *self._absolut_coord(x=a.axis_pos[0] + size, y=a.axis_pos[1] + size),
                fill=fill
            )

    def _absolut_coord(self, x: int or float, y: int or float, origin: Tuple[int, int] = None,
                       factor: float = 2.25, dif: float = 0.0) -> Tuple[int, int]:
        if not origin:
            origin = self.origin
        return int((x * factor + origin[0]) - dif), int((y * factor + origin[1]) - dif)

    def _relative_coord(self, x: int or float, y: int or float, origin: Tuple[int, int] = None,
                        factor: float = 2.25, dif: float = 0.0) -> Tuple[int, int]:
        if not origin:
            origin = self.origin
        return int((x - origin[0]) / factor - dif), int((y - origin[1]) / factor - dif)

    def __sin(self, deg: int or float) -> int or float:
        return np.sin(np.deg2rad(deg))

    def __cos(self, deg: int or float) -> int or float:
        return np.cos(np.deg2rad(deg))

    def __arccos(self, val: int or float) -> float:
        return float(np.degrees(np.arccos(val)))

    def __cos_angle(self, a: float, b: float, c: float) -> float:
        return self.__arccos((a**2 + b**2 - c**2) / (2 * a * b))

    def position(self, ox) -> Pentagon:
        ox: Vector = Vector(ox.x, -ox.y)

        oz: Vector = Vector(*self.arms[0].axis_pos)
        ov: Vector = Vector(*self.arms[1].axis_pos)

        vx: Vector = ox - ov
        xz: Vector = oz - ox

        xv: Vector = ov - ox

        de: float = float(ov // xv + self.__cos_angle(
            xv.length(), self.arms[1].segments[0].length, self.arms[1].segments[1].length
        ))

        ep: float = float(self.__cos_angle(
            self.arms[1].segments[0].length, self.arms[1].segments[1].length, vx.length()
        ))

        ga: float = oz // xz + self.__cos_angle(
            xz.length(), self.arms[0].segments[0].length, self.arms[0].segments[1].length
        )

        be: float = float(self.__cos_angle(
            self.arms[0].segments[0].length, self.arms[0].segments[1].length, xz.length()
        ))

        al: float = float(self.__cos_angle(
            xz.length(), self.arms[0].segments[1].length, self.arms[0].segments[0].length
        ) + ox // (ox - oz) + self.__cos_angle(
            vx.length(), self.arms[1].segments[1].length, self.arms[1].segments[0].length
        ) + ox // vx)

        oy: Vector = Vector(
            self.arms[0].segments[0].length * self.__sin(ga),
            self.arms[0].segments[0].length * self.__cos(ga) + oz.y
        )
        ow: Vector = Vector(
            self.arms[1].segments[0].length * self.__sin(de),
            self.arms[1].segments[0].length * self.__cos(de) + ov.y
        )

        oa: Vector = Vector(0, 0)

        try:
            self.de_angle.set(int(de))
            self.ga_angle.set(int(ga))
        except ValueError:
            pass

        be_1: float = (oy - ox) // (oy - ow)
        ep_1: float = (ow - ox) // (ow - oy)

        return Pentagon(
            ov, ow, ox, oy, oz, oa,
            al, be, be_1, be - be_1, ga, de,
            ep, ep_1, ep - ep_1
        )

    def angles(self, de: int or float, ga: int or float) -> Pentagon:
        ga: float = 180 - ga

        oz: Vector = Vector(*self.arms[0].axis_pos)
        ov: Vector = Vector(*self.arms[1].axis_pos)

        oy: Vector = Vector(
            self.arms[0].segments[0].length * self.__sin(ga),
            self.arms[0].segments[0].length * self.__cos(ga)
        ) + oz
        ow: Vector = Vector(
            self.arms[1].segments[0].length * self.__sin(de),
            self.arms[1].segments[0].length * self.__cos(de)
        ) + ov

        wy: Vector = oy - ow

        ep_1: float = self.__cos_angle(self.arms[1].segments[1].length, wy.length(), self.arms[0].segments[1].length)

        a_length: float = np.sqrt(
            self.arms[1].segments[1].length**2 - (self.arms[0].segments[1].length * self.__sin(ep_1))**2
        )

        oa: Vector = ow + wy * (a_length/wy.length())
        ay: Vector = oy - oa

        ob: Vector = Vector(ay.y, ay.x * -1) + oa
        ab: Vector = ob - oa

        ox: Vector = oa + (ob - oa) * ((self.arms[0].segments[1].length * self.__sin(ep_1)) / ab.length())

        wx: Vector = ox - ow

        be: float = (oz - oy) // (ox - oy)
        be_1: float = (oy - ox) // wy

        ep: float = (ov - ow) // (ox - ow)

        al: float = wx // (ox - oy)

        return Pentagon(
            ov, ow, ox, oy, oz, oa,
            al, be, be_1, be - be_1, ga, de,
            ep, ep_1, ep - ep_1
        )

    def display_pentagon(self, pentagon: Pentagon):
        if not self.pentagon_is_invalid(pentagon):
            self.update(pentagon)

            self.ga_angle.set(pentagon.ga)
            self.de_angle.set(pentagon.de)

    def pentagon_is_invalid(self, p: Pentagon) -> bool:
        p.ga = 180 - p.ga
        angles: tuple = (p.al, p.be, p.ga, p.de, p.ep)

        con1: bool = p.al > 180 or p.be > 180 or p.ep > 180 or sum(angles) != 540
        con2: bool = np.isnan(p.ox.x) or np.isnan(p.ox.y)
        con3: bool = p.ep < p.ep_1 or p.be < p.be_1

        return con1 or con2 or con3

    def update(self, p: Pentagon):

        # Origin:
        self.canvas.create_oval(*self._absolut_coord(x=0, y=0, dif=-5), *self._absolut_coord(x=0, y=0, dif=5), fill="red")

        if "yz" not in self.items.keys():
            self.items["yz"] = self.canvas.create_line(
                *self._absolut_coord(*p.oy.get()), *self._absolut_coord(*p.oz.get()),
                fill="blue", width=3
            )
        else:
            self.canvas.coords(self.items["yz"], *self._absolut_coord(*p.oy.get()), *self._absolut_coord(*p.oz.get()))

        if "vw" not in self.items.keys():
            self.items["vw"] = self.canvas.create_line(
                *self._absolut_coord(*p.ov.get()), *self._absolut_coord(*p.ow.get()),
                fill="red", width=3
            )
        else:
            self.canvas.coords(self.items["vw"], *self._absolut_coord(*p.ov.get()), *self._absolut_coord(*p.ow.get()))

        if "xy" not in self.items.keys():
            self.items["xy"] = self.canvas.create_line(
                *self._absolut_coord(*p.ox.get()), *self._absolut_coord(*p.oy.get()),
                fill="yellow", width=3
            )
        else:
            self.canvas.coords(self.items["xy"], *self._absolut_coord(*p.ox.get()), *self._absolut_coord(*p.oy.get()))

        if "xw" not in self.items.keys():
            self.items["xw"] = self.canvas.create_line(
                *self._absolut_coord(*p.ox.get()), *self._absolut_coord(*p.ow.get()),
                fill="yellow", width=3
            )
        else:
            self.canvas.coords(self.items["xw"], *self._absolut_coord(*p.ox.get()), *self._absolut_coord(*p.ow.get()))

        if "wy" not in self.items.keys():
            self.items["wy"] = self.canvas.create_line(
                *self._absolut_coord(*p.ow.get()), *self._absolut_coord(*p.oy.get()),
                fill="black", width=2
            )
        else:
            self.canvas.coords(self.items["wy"], *self._absolut_coord(*p.ow.get()), *self._absolut_coord(*p.oy.get()))

        if "ax" not in self.items.keys():
            self.items["ax"] = self.canvas.create_line(
                *self._absolut_coord(*p.oa.get()),
                *self._absolut_coord(*p.ox.get()),
                fill="green", width=2
            )
        else:
            self.canvas.coords(
                self.items["ax"],
                *self._absolut_coord(*p.oa.get()),
                *self._absolut_coord(*p.ox.get())
            )

        self.cached_pentagon = p

    def go2(self, x: int or float, y: int or float):
        xx: Vector = (self.cached_pentagon - self.position(Vector(x, y))).ox

        self.canvas.create_line(
            *self._absolut_coord(x, y), *self._absolut_coord(*self.cached_pentagon.ox.get()),
            fill="red", width=3
        )

        print(f'>> finished [{x}, {y}]')

        for i in np.arange(0.0, 1.0, 0.01):
            c: Vector = Vector(x, y) + xx * i
            self.update(self.position(c))
            time.sleep(.1)

    def _simulation(self):
        time.sleep(1.0)

        self.go2(160, 50)

    def start(self):
        if self.ui:
            self.display_pentagon(self.angles(135.0, 135.0))

            t: Thread = Thread(target=self._simulation)
            t.daemon = True
            t.start()

            try:
                self.win.mainloop()
            except KeyboardInterrupt:
                exit(code=0)


if __name__ == "__main__":

    """
    left_arm = Arm(
        axis_pos=(.0, 107.5/2),
        segments=(
            Segment(length=86.5),
            Segment(length=77.0)
        )
    )

    right_arm = Arm(
        axis_pos=(.0, -107.5/2),
        segments=(
            Segment(length=86.5),
            Segment(length=77.0)
        )
    )
    """

    left_arm = Arm(
        axis_pos=(.0, 40/2),
        segments=(
            Segment(length=100.0),
            Segment(length=100.0)
        )
    )

    right_arm = Arm(
        axis_pos=(.0, -40/2),
        segments=(
            Segment(length=100.0),
            Segment(length=100.0)
        )
    )

    sim = Simulator(
        arms=(left_arm, right_arm),
        configuration={
            "geometry": {"width": 800, "height": 600},
            "origin": (200, 300),
            "win pos": f"{-1400}+{150}", #f"{0}+{0}", #
            "bg": "gray",
            "title": "Robotic paint simulator"
        }, ui=True
    )

    sim.start()
