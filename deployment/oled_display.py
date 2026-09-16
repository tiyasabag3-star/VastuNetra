import board
import busio

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import adafruit_ssd1306

WIDTH = 128
HEIGHT = 32

i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(
    WIDTH,
    HEIGHT,


    i2c
)

font = ImageFont.load_default()


def show_result(obj, risk):

    image = Image.new("1", (WIDTH, HEIGHT))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)

    draw.text((0, 0), "AIRPORT AI", font=font, fill=255)

    draw.text((0, 12), f"{obj.upper()}", font=font, fill=255)

    draw.text((0, 22), f"{risk}", font=font, fill=255)

    oled.image(image)
    oled.show()
