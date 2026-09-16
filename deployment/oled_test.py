import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

i2c = busio.I2C(board.SCL, board.SDA)

oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.show()

image = Image.new("1", (128, 64))
draw = ImageDraw.Draw(image)

draw.text((10, 10), "AIRPORT AI", fill=255)
draw.text((10, 30), "SYSTEM READY", fill=255)

oled.image(image)
oled.show()
