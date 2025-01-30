from GameScripts.EntitiesAndComponents.Rectangle import Rectangle
from GameScripts.EntitiesAndComponents.Vector2 import Vector2
import string


class Platform(Rectangle):
    def __init__(self, position: Vector2, size: Vector2, color: string):
        super().__init__(position, size, color)

    def move(self, x: float):
        self.position = self.position.add(Vector2(x, 0))
        if self.position.x < 0:
            self.position.x = 0
        if self.position.x + self.size.x > 94:
            self.position.x = 94 - self.size.x
