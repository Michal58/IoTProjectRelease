import GameScripts.lib.oled.SSD1331 as SSD1331
from PIL import Image, ImageDraw, ImageFont


class Env:
    disp: SSD1331


def setup():
    Env.disp = SSD1331.SSD1331()

    Env.disp.Init()
    Env.disp.clear()


def loop(rectangles):
    image1 = Image.new("RGB", (Env.disp.width, Env.disp.height), "BLACK")
    draw = ImageDraw.Draw(image1)

    for rectangle in rectangles:
        draw.rectangle(rectangle.get_as_list(), fill=rectangle.color)

    Env.disp.ShowImage(image1, 0, 0)


def game_over():
    Env.disp.clear()
