import math


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def add(self, other):
        res = Vector2(self.x, self.y)
        res.x += other.x
        res.y += other.y
        return res

    def subtract(self, other):
        res = Vector2(self.x, self.y)
        res.x -= other.x
        res.y -= other.y
        return res

    def normalize(self):
        length = self.length()
        return Vector2(self.x/length, self.y/length)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)