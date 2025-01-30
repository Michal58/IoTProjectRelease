import string
from GameScripts.EntitiesAndComponents.Vector2 import Vector2


class Rectangle:
    def __init__(self, position: Vector2, size: Vector2, color: string):
        self.position = position
        self.size = size
        self.color = color

    def get_as_list(self):
        x, y = self.position.x, self.position.y
        endPos = self.position.add(self.size)
        width, height = endPos.x, endPos.y
        return [(x, y), (width, height)]

    def overlaps(self, other) -> bool:
        self_left = self.position.x
        self_right = self.position.x + self.size.x
        self_top = self.position.y
        self_bottom = self.position.y + self.size.y

        other_left = other.position.x
        other_right = other.position.x + other.size.x
        other_top = other.position.y
        other_bottom = other.position.y + other.size.y

        return (self_left < other_right and
                self_right > other_left and
                self_top < other_bottom and
                self_bottom > other_top)
