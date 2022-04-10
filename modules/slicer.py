# Friedjof Noweck
# 2021-12-22 Mi
from typing import Tuple, List

from PIL import Image


class Slicer:
    def __init__(self, image: str):
        self.image = Image.open(image)

    def show(self):
        self.image.show()

    def scale(self, *size):
        self.image.thumbnail(size, Image.ANTIALIAS)

    def _get_neighbors(self, x, y, *max_pos) -> Tuple[Tuple[int, int, int, int], ]:
        neighbors: List[Tuple[int, int, int, int], ] = []

        for nx in range(-1, 2):
            for ny in range(-1, 2):
                if max_pos[0] > x + nx >= 0 and max_pos[1] > y + ny >= 0:
                    neighbors.append(self.image.getpixel((x + nx, y + ny)))
                else:
                    neighbors.append((255, 255, 255, 0))

        return tuple(neighbors)

    def _edge(self, neighbors: tuple) -> bool:
        transparent: int = 0
        for n in neighbors:
            if n[:3] == (255, 255, 255):
                transparent += 1

        return neighbors[4][:3] == (0, 0, 0) and transparent >= 3

    def slice(self) -> Image:
        # img: Image = self.image.convert("L")
        img: Image = self.image

        changed_pixel: list = []

        for x in range(img.width):
            xx: list = []
            for y in range(img.height):
                xx.append(self._edge(self._get_neighbors(x, y, img.width, img.height)))
            changed_pixel.append(xx)

        for x in range(img.width):
            for y in range(img.height):
                if changed_pixel[x][y]:
                    img.putpixel((x, y), (*img.getpixel((x, y))[:3], 0))
                else:
                    img.putpixel((x, y), (255, 0, 0, 255))

if __name__ == "__main__":
    s: Slicer = Slicer(r"C:\Users\Friedjof Noweck\Documents\repositories\robotic-painter\images\slicer\example.png")
    s.scale(500, 500)
    s.slice()
    s.show()
