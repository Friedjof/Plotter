# Friedjof Noweck
# 2021-12-11 Sa

from typing import Tuple, List
import numpy as np


class Vector2D:
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
        other: Vector2D = other
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other: Vector2D = other
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if type(other) is int or type(other) is float or type(other) is np.float64:
            return Vector2D(self.x * other, self.y * other)
        else:
            return Vector2D(self.x * other.x, self.y * other.y)

    def __matmul__(self, other) -> float:
        other: Vector2D = other
        return self.x * other.x + self.y * other.y

    def __truediv__(self, other: int or any):
        if type(other) == Vector2D:
            return Vector2D(self.x / other.x, self.y / other.y)
        elif type(other) == int or type(other) == float:
            return Vector2D(self.x / other, self.y / other)

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y

    def __str__(self) -> str:
        return f"<Vector = [x: {round(self.x, 3):>8}, y: {round(self.y, 3):>8}]>"

    def __floordiv__(self, other) -> float:
        return self.__arccos(self @ other / (self.length() * other.length()))


class Vector3D:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def length(self) -> float:
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def get(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

    def __arccos(self, val: int or float) -> float:
        return float(np.degrees(np.arccos(val)))

    def __arcsin(self, val: int or float) -> float:
        return float(np.degrees(np.arcsin(val)))

    def __add__(self, other):
        other: Vector2D = other
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        other: Vector3D = other
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if type(other) is int or type(other) is float or type(other) is np.float64:
            return Vector3D(self.x * other, self.y * other, self.z * other)
        else:
            return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)

    def __matmul__(self, other) -> float:
        other: Vector3D = other
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, other: int or any):
        if type(other) == Vector3D:
            return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)
        elif type(other) == int or type(other) == float:
            return Vector3D(self.x / other, self.y / other, self.z / other)

    def __getitem__(self, item: int) -> float:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z

    def __str__(self) -> str:
        return f"<Vector3D = [x: {round(self.x, 3):>5}, y: {round(self.y, 3):>5}, z: {round(self.z, 3):>5}]>"

    def __floordiv__(self, other) -> float:
        return self.__arccos(self @ other / (self.length() * other.length()))

    def __mod__(self, other) -> float:
        return self.__arcsin(abs(self @ other) / (self.length() * other.length()))

    def __abs__(self) -> Vector2D:
        return Vector2D(x=abs(self.x), y=abs(self.y))

    def __or__(self, other):
        v: Vector3D = other

        return Vector3D(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x
        )


class Flat:
    def __init__(self, support_vector: Vector3D, span_vectors: Tuple[Vector3D, Vector3D]):
        self.support_vector = support_vector
        self.span_vectors = span_vectors


class Line:
    def __init__(self, support_vector: Vector2D, length_vector: Vector2D):
        self.support_vector = support_vector
        self.length_vector = length_vector

    def ox(self, factor: Vector2D or int) -> Vector2D:
        return self.support_vector + self.length_vector * factor


class Angle2D:
    def __init__(self, angle: float or int):
        self.angle = angle
        self.M: Matrix2X2 = Matrix2X2(
            [np.cos(np.deg2rad(self.angle)), np.sin(np.deg2rad(self.angle))],
            [np.sin(np.deg2rad(self.angle)), -np.cos(np.deg2rad(self.angle))]
        )

    def __mul__(self, other: Vector2D) -> Vector2D:
        return self.M * other


class Matrix2X2:
    def __init__(self, x: List, y: List):
        self.x: List = x
        self.y: List = y

    def __mul__(self, other: Vector2D) -> Vector2D:
        return Vector2D(
            x=self.x[0] * other.x + self.y[0] * other.y,
            y=self.x[1] * other.x + self.y[1] * other.y
        )


if __name__ == "__main__":
    # The circle
    print("Aufgabe 1")
    a: Vector3D = Vector3D(-2, -3, 4)
    b: Vector3D = Vector3D(0, 2, -4)

    print(f"Winkel zwischen a und b = {a // b}°")

    print("---\nAufgabe 2")
    oa: Vector3D = Vector3D(-1, 0, 2)
    ob: Vector3D = Vector3D(2, 4, 2)
    oc: Vector3D = Vector3D(-5, 3, 10)

    print(f"|ab| = {(ob - oa).length()}LE, |ac| = {(oc - oa).length()}LE, |bc| = {(oc - ob).length()}LE")

    print(f"Rechter Winkel an A = {(ob - oa) @ (oc - oa) == 0.0}")

    print(f"Winekl A = {(ob - oa) // (oc - oa)}°")
    print(f"Winkel B = {(oa - ob) // (oc - ob)}°")
    print(f"Winkel C = {(oa - oc) // (ob - oc)}°")

    print(f"Fläche = {(oa - ob).length() * (oa - oc).length() / 2}FE")

    print("---\nAufgabe 3")
    a: Vector3D = Vector3D(1, 4, 2)
    b: Vector3D = Vector3D(-5, 2, -1)

    print(f"Winkel a) = {a // b}°")

    a: Vector3D = Vector3D(2, -2, 3)
    b: Vector3D = Vector3D(0, 7, -3)

    print(f"Winkel b) = {a // b}°")

    print("---\nAufgabe 4")
    a: Vector3D = Vector3D(3, -1, 8)
    b: Vector3D = Vector3D(1, 4, 2)

    print(f"a) = {a // b}°")

    a: Vector3D = Vector3D(1, 0, -3) | Vector3D(-3, -2)
    b: Vector3D = Vector3D(3, 2, -1) | Vector3D(0, -2, 5)

    print(f"b) = {a // b}°")

    print("---\nAufgabe 5")
    a: Vector3D = Vector3D(4, -2, 7)
    b: Vector3D = Vector3D(3, -6, -1)

    print(f"Winkel a % b = {a % b}°")

    print("---\nAufgabe 6")
    oa: Vector3D = Vector3D(2, -2)
    ob: Vector3D = Vector3D(2, 2)
    oc: Vector3D = Vector3D(-2, 2)
    od: Vector3D = Vector3D(-2, -2)
    os: Vector3D = Vector3D(z=6)

    print(f"Winkel Alpha = {(os - oa) // (os - ob)}°")
    print(f"Winkel Beta = {(ob - oa) // (oc - oa)}°")
    print(f"Winkel µ = {os // (os - ob)}°")

    print(Vector3D(-3, -1, 8) | Vector3D(-5, -3, 7))
