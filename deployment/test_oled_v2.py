from oled_display import show_result
import time

objects = [

    ("Knife", "THREAT"),
    ("Empty", "SAFE"),
    ("Keys", "SUSPICIOUS"),
    ("Battery", "SUSPICIOUS")

]

while True:

    for obj, risk in objects:

        show_result(obj, risk)

        time.sleep(2)
