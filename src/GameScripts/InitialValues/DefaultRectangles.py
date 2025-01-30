from GameScripts.EntitiesAndComponents.Brick import Brick
from GameScripts.EntitiesAndComponents.Vector2 import Vector2
from GameScripts.EntitiesAndComponents.Platform import Platform
from GameScripts.EntitiesAndComponents.Ball import Ball

default_bricks = [
    Brick(Vector2(0, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(10, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(20, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(30, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(40, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(50, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(60, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(70, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(80, 5), Vector2(10, 5), "RED", 5),
    Brick(Vector2(90, 5), Vector2(10, 5), "RED", 5),

    Brick(Vector2(0, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(10, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(20, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(30, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(40, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(50, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(60, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(70, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(80, 12), Vector2(10, 5), "ORANGE", 3),
    Brick(Vector2(90, 12), Vector2(10, 5), "ORANGE", 3),

    Brick(Vector2(0, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(10, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(20, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(30, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(40, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(50, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(60, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(70, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(80, 19), Vector2(10, 5), "YELLOW", 1),
    Brick(Vector2(90, 19), Vector2(10, 5), "YELLOW", 1),
]

default_platform = Platform(Vector2(45, 60), Vector2(20, 5), "GRAY")

default_ball = Ball(Vector2(45, 55), Vector2(5, 5), "WHITE")
