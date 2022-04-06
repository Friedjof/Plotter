# Friedjof Noweck
# 2021-12-11 Sa
from typing import Tuple

import numpy as np


class Vector:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x: float = x
        self.y: float = y

    def length(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)

    def get(self) -> Tuple[float, float]:
        return self.x, self.y

    def __arccos(self, val: int or float) -> float:
        return float(np.degrees(np.arccos(val)))

    def __add__(self, other):
        other: Vector = other
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other: Vector = other
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) is int or type(other) is float or type(other) is np.float64:
            return Vector(self.x * other, self.y * other)
        else:
            return Vector(self.x * other.x, self.y * other.y)

    def __matmul__(self, other) -> float:
        other: Vector = other
        return self.x * other.x + self.y * other.y

    def __truediv__(self, other: int or any):
        if type(other) == Vector:
            return Vector(self.x / other.x, self.y / other.y)
        elif type(other) == int or type(other) == float:
            return Vector(self.x / other, self.y / other)

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y

    def __str__(self) -> str:
        return f"<Vector = [x: {round(self.x, 3):>8}, y: {round(self.y, 3):>8}]>"

    def __floordiv__(self, other) -> float:
        return self.__arccos(self @ other / (self.length() * other.length()))


if __name__ == "__main__":
    oa = Vector(1, 1)
    ob = Vector(2, 2)

    print(oa @ ob)

    oc: Vector = oa / ob
    print(oc)

    oc: Vector = oa / 4.33
    print(oc)
