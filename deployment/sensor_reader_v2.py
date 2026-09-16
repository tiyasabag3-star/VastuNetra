from smbus2 import SMBus
import subprocess
import re
import math
import time

# ==============================
# I2C Configuration
# ==============================
MUX_ADDR = 0x70
QMC_ADDR = 0x0D

bus = SMBus(1)

SAMPLES = 20


def select_channel(channel):
    bus.write_byte(MUX_ADDR, 1 << channel)
    time.sleep(0.02)


def init_qmc():
    bus.write_byte_data(QMC_ADDR, 0x0B, 0x01)
    bus.write_byte_data(QMC_ADDR, 0x09, 0x1D)
    time.sleep(0.02)


def read_word(reg):
    low = bus.read_byte_data(QMC_ADDR, reg)
    high = bus.read_byte_data(QMC_ADDR, reg + 1)

    value = (high << 8) | low

    if value > 32767:
        value -= 65536

    return value


def read_sensor(channel):
    try:
        select_channel(channel)
        init_qmc()

        xs = []
        ys = []
        zs = []

        for _ in range(SAMPLES):
            xs.append(read_word(0x00))
            ys.append(read_word(0x02))
            zs.append(read_word(0x04))
            time.sleep(0.005)

        x = sum(xs) / SAMPLES
        y = sum(ys) / SAMPLES
        z = sum(zs) / SAMPLES

        magnitude = math.sqrt(x*x + y*y + z*z)

        return {
            "status": "Connected",
            "x": x,
            "y": y,
            "z": z,
            "magnitude": magnitude
        }

    except Exception:
        return {
            "status": "Not Connected",
            "x": 0,
            "y": 0,
            "z": 0,
            "magnitude": 0
        }


def get_all_sensors():
    sensors = {}

    for ch in range(4):
        sensors[f"sensor{ch+1}"] = read_sensor(ch)

    return sensors


def get_rssi():
    try:
        output = subprocess.check_output(
            "iw dev wlan0 link",
            shell=True
        ).decode()

        match = re.search(r"signal:\s*(-?\d+)", output)

        if match:
            return int(match.group(1))

    except Exception:
        pass

    return -100


if __name__ == "__main__":

    while True:

        sensors = get_all_sensors()

        print("=" * 60)

        for i in range(1, 5):
            s = sensors[f"sensor{i}"]

            print(f"Sensor {i}")
            print(f"Status    : {s['status']}")
            print(f"X         : {s['x']:.2f}")
            print(f"Y         : {s['y']:.2f}")
            print(f"Z         : {s['z']:.2f}")
            print(f"Magnitude : {s['magnitude']:.2f}")
            print()

        print("RSSI:", get_rssi())
        time.sleep(1)
