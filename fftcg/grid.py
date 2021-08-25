from __future__ import annotations


class Grid(tuple[int, int]):
    def __mul__(self, other: Grid) -> Grid:
        return Grid((self.x * other.x, self.y * other.y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def capacity(self):
        # capacity of grid (reserve last space for card back)
        return self.x * self.y - 1
