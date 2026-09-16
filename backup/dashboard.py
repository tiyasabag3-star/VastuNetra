from sensor_reader import get_magnetometer, get_rssi
from feature_extractor import extract_features
from ai_engine import predict_threat
import time

while True:

    samples = []

    for i in range(20):
        samples.append(get_magnetometer())
        time.sleep(0.1)

    features = extract_features(samples, get_rssi())

    prediction, confidence = predict_threat(features)

    print("\n========================")
    print("FEATURES:")
    print(features)
    print("\nPREDICTION:", prediction)
    print("CONFIDENCE:", round(confidence, 2), "%")
    print("========================")

    time.sleep(2)
