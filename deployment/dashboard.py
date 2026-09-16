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

while True:
    try:
        sensors = get_all_sensors()
        rssi = get_rssi()

        # Extract Features
        features = extract_features(sensors, rssi)

        # AI Prediction
        prediction, confidence = predict_threat(features)

        # =====================================
        # Empty Tray Detection
        # =====================================
        m1 = features["mag_1"]
        m2 = features["mag_2"]
        m3 = features["mag_3"]

        # Adjusted using your live empty readings
        if (
            1750 <= m1 <= 1900 and
            2420 <= m2 <= 2550 and
            2600 <= m3 <= 2750
        ):
            prediction = "empty"
            confidence = 100.0

        # Debug
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

        for k, v in features.items():
            print(f"{k:20}: {v}")

        print("\nPrediction :", prediction)
        print("Confidence :", round(confidence, 2), "%")

        # OLED Display
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
