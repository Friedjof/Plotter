# Friedjof Noweck
# 2021-12-08 Mi
import random
import time
from threading import Thread
from tkinter import *
from typing import Tuple

import numpy as np

from modules.arm import Segment, Arm, Pentagon
from modules.vectors import Vector2D, Line, Angle2D


class Simulator:
    def __init__(self, arms: Tuple[Arm, Arm], configuration: dict, ui: bool = True):
        self.arms = arms
        self.configs = configuration
        self.origin: Tuple[int, int] = self.configs["origin"]
        self.ui = ui

        self.current_pentagon: Pentagon = self.angles(135.0, 135.0)

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
            Vector2D(*self._relative_coord(event.x, event.y))
        )

        self.display(pentagon=p)

    def _update_degree(self, event):
        p: Pentagon = self.angles(self.de_angle.get(), self.ga_angle.get())

        self.display(pentagon=p)

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
        return int((x - origin[0]) / factor - dif), int((y - origin[1]) * (-1) / factor - dif)

    def __sin(self, deg: int or float) -> int or float:
        return np.sin(np.deg2rad(deg))

    def __cos(self, deg: int or float) -> int or float:
        return np.cos(np.deg2rad(deg))

    def __arccos(self, val: int or float) -> float:
        return float(np.degrees(np.arccos(val)))

    def __cos_angle(self, a: float, b: float, c: float) -> float:
        return self.__arccos((a**2 + b**2 - c**2) / (2 * a * b))

    def position(self, ox) -> Pentagon:
        ox: Vector2D = Vector2D(ox.x, -ox.y)

        oz: Vector2D = Vector2D(*self.arms[0].axis_pos)
        ov: Vector2D = Vector2D(*self.arms[1].axis_pos)

        vx: Vector2D = ox - ov
        xz: Vector2D = oz - ox

        xv: Vector2D = ov - ox

        de: float = float(ov // xv + self.__cos_angle(
            xv.length(), self.arms[1].segments[0].length, self.arms[1].segments[1].length
        ))

        ep: float = float(self.__cos_angle(
            self.arms[1].segments[0].length, self.arms[1].segments[1].length, vx.length()
        ))

        ga: float = 180 - (oz // xz + self.__cos_angle(
            xz.length(), self.arms[0].segments[0].length, self.arms[0].segments[1].length
        ))

        be: float = float(self.__cos_angle(
            self.arms[0].segments[0].length, self.arms[0].segments[1].length, xz.length()
        ))

        al: float = float(self.__cos_angle(
            xz.length(), self.arms[0].segments[1].length, self.arms[0].segments[0].length
        ) + ox // (ox - oz) + self.__cos_angle(
            vx.length(), self.arms[1].segments[1].length, self.arms[1].segments[0].length
        ) + ox // vx)

        oy: Vector2D = Vector2D(
            self.arms[0].segments[0].length * self.__sin(ga),
            self.arms[0].segments[0].length * self.__cos(ga) + oz.y
        )
        ow: Vector2D = Vector2D(
            self.arms[1].segments[0].length * self.__sin(de),
            self.arms[1].segments[0].length * self.__cos(de) + ov.y
        )

        oa: Vector2D = Vector2D(0, 0)

        be_1: float = (oy - ox) // (oy - ow)
        ep_1: float = (ow - ox) // (ow - oy)

        return Pentagon(
            ov, ow, ox, oy, oz, oa,
            al, be, be_1, be - be_1, ga, de,
            ep, ep_1, ep - ep_1
        )

    def angles(self, de: int or float, ga: int or float) -> Pentagon:
        ga: float = 180 - ga

        oz: Vector2D = Vector2D(*self.arms[0].axis_pos)
        ov: Vector2D = Vector2D(*self.arms[1].axis_pos)

        oy: Vector2D = Vector2D(
            self.arms[0].segments[0].length * self.__sin(ga),
            self.arms[0].segments[0].length * self.__cos(ga)
        ) + oz
        ow: Vector2D = Vector2D(
            self.arms[1].segments[0].length * self.__sin(de),
            self.arms[1].segments[0].length * self.__cos(de)
        ) + ov

        wy: Vector2D = oy - ow

        ep_1: float = self.__cos_angle(self.arms[1].segments[1].length, wy.length(), self.arms[0].segments[1].length)

        a_length: float = np.sqrt(
            self.arms[1].segments[1].length**2 - (self.arms[0].segments[1].length * self.__sin(ep_1))**2
        )

        oa: Vector2D = ow + wy * (a_length / wy.length())
        ay: Vector2D = oy - oa

        ob: Vector2D = Vector2D(ay.y, ay.x * -1) + oa
        ab: Vector2D = ob - oa

        ox: Vector2D = oa + (ob - oa) * ((self.arms[0].segments[1].length * self.__sin(ep_1)) / ab.length())

        wx: Vector2D = ox - ow

        be: float = (oz - oy) // (ox - oy)
        be_1: float = (oy - ox) // wy

        ep: float = (ov - ow) // (ox - ow)

        al: float = wx // (ox - oy)

        return Pentagon(
            ov, ow, ox, oy, oz, oa,
            al, be, be_1, be - be_1, ga, de,
            ep, ep_1, ep - ep_1
        )

    def update(self, p: Pentagon):
        if "origin" not in self.items.keys():
            self.items["origin"] = self.canvas.create_oval(
                *self._absolut_coord(x=0, y=0, dif=-5),
                *self._absolut_coord(x=0, y=0, dif=5), fill="red"
            )

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

        self.current_pentagon = p

    def display(self, pentagon: Pentagon):
        if not pentagon.is_invalid():
            self.update(pentagon)

            self.ga_angle.set(int(180 - pentagon.ga))
            self.de_angle.set(int(pentagon.de))

    def go2(self, x: int or float, y: int or float, time_per_tick: float = .1, support_line: bool = False):
        y: int or float = -y
        support_vector: Vector2D = Vector2D(self.current_pentagon.ox.x, -self.current_pentagon.ox.y)
        ox = Vector2D(x, y) - support_vector

        if support_line:
            sl: int = self.canvas.create_line(
                *self._absolut_coord(support_vector.x, -support_vector.y),
                *self._absolut_coord(support_vector.x, -support_vector.y),
                fill="black", width=5
            )
        else:
            sl: int = 0

        l: Line = Line(support_vector=support_vector, length_vector=ox)

        for i in np.arange(0.0, ox.length(), 1.6):
            p: Pentagon = self.position(
                l.ox(i / ox.length())
            )
            self.display(p)

            if support_line:
                self.canvas.coords(
                    sl, *self._absolut_coord(support_vector.x, -support_vector.y),
                    *self._absolut_coord(*p.ox.get())
                )

            time.sleep(time_per_tick)

        self.display(self.position(Vector2D(x, y)))
        # self.canvas.itemconfigure(l, state='hidden')

    def __arc(self, radius: Vector2D, support_vector: Vector2D, center_dot: bool, dots: list = (), **angles):
        if center_dot:
            dots.append(self.canvas.create_oval(
                *self._absolut_coord(x=support_vector.x, y=support_vector.y, dif=-6),
                *self._absolut_coord(x=support_vector.x, y=support_vector.y, dif=6), fill="red"
            ))

        for angle in np.arange(angles["from"], angles["to"], angles["steps"]):
            yield Angle2D(angle=angle) * radius + support_vector

    def _simulation(self):
        time.sleep(1.0)

        speed: float = 0.01

        elements: list = []

        time.sleep(2)

        self.go2(190, 0, time_per_tick=speed, support_line=False)
        self.go2(70, 0, time_per_tick=speed, support_line=False)

        for n in self.__arc(
            radius=Vector2D(0, 120),
            support_vector=Vector2D(30, 0),
            center_dot=False,
            **{"from": 0, "to": 180, "steps": 15}
        ):
            self.go2(n.x, n.y, time_per_tick=speed, support_line=False)

        for n in self.__arc(
            radius=Vector2D(0, -50),
            support_vector=Vector2D(30, 0),
            center_dot=False,
            **{"from": 360, "to": 180, "steps": -5}
        ):
            self.go2(n.x, n.y, time_per_tick=speed, support_line=False)

        while True:
            for i, n in enumerate(self.__arc(
                    radius=Vector2D(random.randint(10, 30), 0),
                    support_vector=Vector2D(random.randint(100, 150), random.randint(-75, 75)),
                    center_dot=True, dots=elements,
                    **{"from": 0, "to": 360, "steps": 4}
                )
            ):
                if i > 1:
                    self.go2(n.x, n.y, time_per_tick=speed, support_line=False)
                else:
                    self.go2(n.x, n.y, time_per_tick=speed * .5, support_line=False)

                elements.append(self.canvas.create_oval(
                    *self._absolut_coord(x=n.x, y=n.y, dif=-1),
                    *self._absolut_coord(x=n.x, y=n.y, dif=1),
                    fill="white", outline="white"
                ))

            for d in elements:
                self.canvas.delete(d)

    def _sin_plot(self):
        dots: list = []
        speed: float = 0.001

        while True:
            for i in range(1, 5):
                for x in np.arange(100, 190, .5):
                    if (i % 2) == 0:
                        y: float = self.__sin(10 * x) * (i * 8 + 10)
                    else:
                        x: int = 290 - x
                        y: float = self.__sin(10 * x) * (i * 8 + 10)

                    self.go2(x, y, time_per_tick=speed, support_line=False)

                    dots.append(self.canvas.create_oval(
                        *self._absolut_coord(x=x, y=y, dif=-2),
                        *self._absolut_coord(x=x, y=y, dif=2),
                        fill="white", outline="white"
                    ))

                for d in dots:
                    self.canvas.delete(d)

    def start(self):
        if self.ui:
            self.display(self.angles(135.0, 135.0))

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
            "geometry": {"width": 1000, "height": 700},
            "origin": (200, 350),
            "win pos": f"{0}+{0}",
            "bg": "gray",
            "title": "Robotic paint simulator"
        }, ui=True
    )

    sim.start()
