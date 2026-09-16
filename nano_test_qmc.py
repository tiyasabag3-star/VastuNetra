from smbus2 import SMBus
import time

PCA_ADDR = 0x70
ADDR = 0x0D

bus = SMBus(1)

bus.write_byte(PCA_ADDR, 0x02)


time.sleep(0.1)


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

while True:
    x = read_word(0x00)
    y = read_word(0x02)
    z = read_word(0x04)

    print(f"X={x}  Y={y}  Z={z}")
    time.sleep(0.5)
