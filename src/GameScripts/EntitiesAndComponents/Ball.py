from GameScripts.EntitiesAndComponents.Rectangle import Rectangle
from GameScripts.EntitiesAndComponents.Vector2 import Vector2
import string


class Ball(Rectangle):
    def __init__(self, position: Vector2, size: Vector2, color: string):
        super().__init__(position, size, color)
        self.direction = Vector2(0, 0)

    def move(self):
        self.position = self.position.add(Vector2(self.direction.x * 5, self.direction.y * 5))

    def is_moving(self):
        return self.direction.length() != 0
