import time
import copy

from GameScripts.Systems import Draw, Physics
from GameScripts.InitialValues.DefaultRectangles import default_bricks, default_platform, default_ball


def game():
    bricks = copy.deepcopy(default_bricks)
    platform = copy.deepcopy(default_platform)
    ball = copy.deepcopy(default_ball)
    score = 0

    Draw.setup()
    while True:
        Draw.loop(bricks + [platform, ball])
        score_change = Physics.loop(bricks, platform, ball)
        if score_change == -1:
            return score
        else:
            score += score_change
