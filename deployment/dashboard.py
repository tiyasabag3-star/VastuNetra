from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features
from ai_engine import predict_threat
import time
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw

# =====================================
# OLED Setup
# =====================================
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

print("=" * 60)
print("      AIRPORT AI THREAT DETECTION DASHBOARD")
print("=" * 60)

# =====================================
# AUTO CALIBRATION
# Keep the tray EMPTY while the program starts
# =====================================
print("\nCalibrating... Please keep the tray EMPTY.")
time.sleep(2)

samples = []

for _ in range(10):
    sensors = get_all_sensors()

    samples.append([
        sensors["sensor1"]["magnitude"],
        sensors["sensor2"]["magnitude"],
        sensors["sensor3"]["magnitude"]
    ])

    time.sleep(0.2)

EMPTY_MAG1 = sum(s[0] for s in samples) / len(samples)
EMPTY_MAG2 = sum(s[1] for s in samples) / len(samples)
EMPTY_MAG3 = sum(s[2] for s in samples) / len(samples)

TOL = 180

print("\nCalibration Complete!")
print(f"Empty Signature:")
print(f"Sensor1 = {EMPTY_MAG1:.2f}")
print(f"Sensor2 = {EMPTY_MAG2:.2f}")
print(f"Sensor3 = {EMPTY_MAG3:.2f}")

while True:
    try:
        sensors = get_all_sensors()
        rssi = get_rssi()

        # =====================================
        # Feature Extraction
        # =====================================
        features = extract_features(sensors, rssi)

        # =====================================
        # AI Prediction
        # =====================================
        prediction, confidence = predict_threat(features)

        # =====================================
        # Empty Tray Detection
        # =====================================
        m1 = features["mag_1"]
        m2 = features["mag_2"]
        m3 = features["mag_3"]

        if (
            abs(m1 - EMPTY_MAG1) <= TOL and
            abs(m2 - EMPTY_MAG2) <= TOL and
            abs(m3 - EMPTY_MAG3) <= TOL
        ):
            prediction = "empty"
            confidence = 100.0

        # =====================================
        # Debug Output
        # =====================================
        print("\n==============================")
        print("AI RETURNED")
        print("==============================")
        print("Prediction :", prediction)
        print("Confidence :", confidence)

        print("\n" + "=" * 50)
        print("Sensor Readings")
        print("=" * 50)

        for i in range(1, 5):
            sensor = sensors[f"sensor{i}"]

            print(f"\nSensor {i}")
            print(f"Status    : {sensor['status']}")
            print(f"X         : {sensor['x']}")
            print(f"Y         : {sensor['y']}")
            print(f"Z         : {sensor['z']}")
            print(f"Magnitude : {sensor['magnitude']:.2f}")

        print(f"\nRSSI : {rssi}")

        print("\nExtracted Features")
        print("-" * 50)

        for key, value in features.items():
            print(f"{key:20}: {value}")

        print("\nPrediction :", prediction)
        print("Confidence :", round(confidence, 2), "%")

        # =====================================
        # OLED Display
        # =====================================
        image = Image.new("1", (128, 32))
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), prediction.upper(), fill=255)
        draw.text((0, 16), f"{confidence:.1f}%", fill=255)

        oled.fill(0)
        oled.image(image)
        oled.show()

    except Exception as e:
        print("Error:", e)

    time.sleep(2)
