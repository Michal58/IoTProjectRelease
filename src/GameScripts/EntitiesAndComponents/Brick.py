import string

from GameScripts.EntitiesAndComponents.Rectangle import Rectangle
from GameScripts.EntitiesAndComponents.Vector2 import Vector2


class Brick(Rectangle):
    def __init__(self, position: Vector2, size: Vector2, color: string, point_worth: int):
        super().__init__(position, size, color)
        self.point_worth = point_worth
