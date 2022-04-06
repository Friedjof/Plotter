# Friedjof Noweck
# 2021-12-08 Mi
from typing import Tuple

import numpy as np

from modules.vectors import Vector


class Segment:
    def __init__(self, length: float):
        self.length = length

    def __str__(self) -> str:
        return f"{self.length}"


class Arm:
    def __init__(self, axis_pos: Tuple[float, float], segments: Tuple[Segment, Segment]):
        self.segments = segments
        self.axis_pos = axis_pos

    def __str__(self) -> str:
        return f"{self.axis_pos} - Segments: {', '.join(f'{i}: {s}' for i, s in enumerate(self.segments))}"


class Pentagon:
    def __init__(
            self, ov: Vector, ow: Vector, ox: Vector, oy: Vector, oz: Vector, oa: Vector,
            al: float, be: float, be_1: float, be_2: float, ga: float, de: float,
            ep: float, ep_1: float, ep_2: float
    ):
        self.ov: Vector = ov
        self.ow: Vector = ow
        self.ox: Vector = ox
        self.oy: Vector = oy
        self.oz: Vector = oz
        self.oa: Vector = oa

        self.al: float = al
        self.be: float = be
        self.be_1: float = be_1
        self.be_2: float = be_2

        self.ga: float = ga
        self.de: float = de
        self.de: float = de
        self.ep: float = ep
        self.ep_1: float = ep_1
        self.ep_2: float = ep_2

    def __floordiv__(self, other, steps: float = 1.0) -> Tuple[tuple, tuple]:
        p: Pentagon = other
        dif: Pentagon = self - p

        max_dif: float = max((dif.ga, dif.de))

        ga_steps: float = (dif.ga / max_dif) * steps
        de_steps: float = (dif.de / max_dif) * steps

        print(dif.ga, dif.de)

        return tuple(np.arange(
            self.ga, p.ga, ga_steps if dif.ga < 0.0 else -ga_steps
        )), tuple(np.arange(
            self.de, p.de, de_steps if dif.de < 0.0 else -de_steps
        ))

    def __sub__(self, other):
        p: Pentagon = other

        return Pentagon(
            self.ov - p.ov,
            self.ow - p.ow,
            self.ox - p.ox,
            self.oy - p.oy,
            self.oz - p.oz,
            self.oa - p.oa,

            self.al - p.al,
            self.be - p.be,
            self.be_1 - p.be_1,
            self.be_2 - p.be_2,

            self.ga - p.ga,
            self.de - p.de,
            self.ep - p.ep,
            self.ep_1 - p.ep_1,
            self.ep_2 - p.ep_2
        )

    def __str__(self) -> str:
        return f"<Pentagon: de: {self.de:.2f}°, ga: {self.ga:.2f}°, ox: {self.ox}>"
