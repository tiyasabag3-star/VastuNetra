from smbus2 import SMBus
import subprocess
import re
import math

ADDR = 0x0D

bus = SMBus(1)

# Initialize QMC5883L
bus.write_byte_data(ADDR, 0x0B, 0x01)
bus.write_byte_data(ADDR, 0x09, 0x1D)

def read_word(reg):
    low = bus.read_byte_data(ADDR, reg)
    high = bus.read_byte_data(ADDR, reg + 1)

    value = (high << 8) | low

    if value > 32767:
        value -= 65536

    return value

def get_magnetometer():

    x = read_word(0x00)
    y = read_word(0x02)
    z = read_word(0x04)

    magnitude = math.sqrt(x*x + y*y + z*z)

    return {
        "x": x,
        "y": y,
        "z": z,
        "magnitude": magnitude
    }

def get_rssi():

    try:
        output = subprocess.check_output(
            "iw dev wlan0 link",
            shell=True
        ).decode()

        match = re.search(r"signal:\s*(-\d+)", output)

        if match:
            return int(match.group(1))

    except:
        pass

    return -100

if __name__ == "__main__":

    data = get_magnetometer()

    print("X:", data["x"])
    print("Y:", data["y"])
    print("Z:", data["z"])
    print("Magnitude:", round(data["magnitude"],2))
    print("RSSI:", get_rssi())
