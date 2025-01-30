import RPi.GPIO as GPIO
from GameScripts.EntitiesAndComponents.Vector2 import Vector2

from config import *
import time

wasEventAdded = False

wasEncoderRised = False
wasEncoderRight = False

def move(platform, ball):
    move_value = 0
    if(GPIO.input(buttonRed) == 1):
        move_value += 1
    if(GPIO.input(buttonGreen) == 1):
        move_value -= 1

    platform.move(move_value * 10)
    if move_value != 0 and not ball.is_moving():
        ball.direction = Vector2(move_value, -1).normalize()
    ball.move()


def collisions(bricks, platform, ball):
    if ball.position.y > 60:
        return -1

    if ball.overlaps(platform):
        ball.direction = ball.position.subtract(platform.position).normalize()
        return 0

    if ball.position.y < 0:
        ball.direction.y = -ball.direction.y

    if ball.position.x < 0 and ball.direction.x < 0:
        ball.direction.x = -ball.direction.x
        
    if ball.position.x > 92 and ball.direction.x > 0:
        ball.direction.x = -ball.direction.x

    for brick in bricks:
        if ball.overlaps(brick):
            bricks.remove(brick)
            ball.direction = ball.position.subtract(brick.position).normalize()
            if len(bricks) == 0:
                return -1
            return brick.point_worth
    return 0


def loop(bricks, platform, ball):
    move(platform, ball)
    return collisions(bricks, platform, ball)
