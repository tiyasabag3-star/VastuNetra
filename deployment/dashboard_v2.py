from oled_display import show_result
from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features
from ai_engine_v2 import predict_object
import time
import os

# =====================================================
# Risk Levels
# =====================================================
def get_risk(prediction):
    prediction = prediction.lower()

    safe = [
        "empty",
        "spoon",
        "fork"
    ]

    suspicious = [
        "keys",
        "usb_adapter",
        "battery"
    ]

    threat = [
        "knife",
        "scissors",
        "screwdriver",
        "nail cutter"
    ]

    if prediction in safe:
        return "SAFE"
    elif prediction in suspicious:
        return "SUSPICIOUS"
    elif prediction in threat:
        return "THREAT"

    return "UNKNOWN"


# =====================================================
# Confidence Status
# =====================================================
def confidence_status(conf):
    if conf >= 95:
        return "VERY HIGH"
    elif conf >= 85:
        return "HIGH"
    elif conf >= 70:
        return "MEDIUM"
    else:
        return "LOW"


# =====================================================
# Sensor Bar
# =====================================================
def sensor_bar(value, max_value):
    length = 25

    if max_value == 0:
        return "-" * length

    filled = int((value / max_value) * length)

    return "█" * filled + "-" * (length - filled)


# =====================================================
# Main Loop
# =====================================================
while True:

    os.system("clear")

    sensors = get_all_sensors()
    rssi = get_rssi()

    features = extract_features(
        sensors,
        rssi
    )

    # -----------------------------------------
    # AI Prediction
    # -----------------------------------------
    prediction, confidence = predict_object(features)

    # -----------------------------------------
    # Empty Tray Detection
    # -----------------------------------------
    m1 = features["mag_1"]
    m2 = features["mag_2"]
    m3 = features["mag_3"]

    if (
        1750 <= m1 <= 1900 and
        2420 <= m2 <= 2550 and
        2600 <= m3 <= 2750
    ):
        prediction = "empty"
        confidence = 100.0

    # -----------------------------------------
    # Risk
    # -----------------------------------------
    risk = get_risk(prediction)

    mags = [
        sensors["sensor1"]["magnitude"],
        sensors["sensor2"]["magnitude"],
        sensors["sensor3"]["magnitude"],
        sensors["sensor4"]["magnitude"]
    ]

    max_mag = max(mags)

    strongest = mags.index(max_mag) + 1 if max_mag > 0 else 0

    print("=" * 65)
    print("        AIRPORT AI THREAT DETECTION SYSTEM V2.0")
    print("=" * 65)
    print()

    print(f"OBJECT DETECTED : {prediction.upper()}")
    print(f"THREAT LEVEL    : {risk}")
    print(f"CONFIDENCE      : {confidence:.2f} %")
    print(f"MODEL STATUS    : {confidence_status(confidence)}")

    print()
    print("-" * 65)

    if strongest != 0:
        print(f"STRONGEST SENSOR : SENSOR {strongest}")
    else:
        print("STRONGEST SENSOR : NONE")

    print("-" * 65)

    for i in range(4):
        print(
            f"S{i+1}  "
            f"{sensor_bar(mags[i], max_mag)} "
            f"{mags[i]:.1f}"
        )

    print("-" * 65)
    print()

    print("GLOBAL FEATURES")
    print(f"Average Magnitude : {features['avg_mag']:.2f}")
    print(f"Maximum Magnitude : {features['max_mag']:.2f}")
    print(f"Minimum Magnitude : {features['min_mag']:.2f}")
    print(f"Range             : {features['range_mag']:.2f}")
    print(f"Std Deviation     : {features['std_mag']:.2f}")
    print(f"RSSI              : {rssi} dBm")
    print()

    if risk == "THREAT":
        print("🚨 ACTION : STOP AND INSPECT LUGGAGE")
    elif risk == "SUSPICIOUS":
        print("⚠️ ACTION : MANUAL VERIFICATION")
    else:
        print("✅ ACTION : CLEAR")

    print()
    print("=" * 65)

    show_result(prediction, risk)

    time.sleep(2)
