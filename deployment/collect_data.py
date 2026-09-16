from sensor_reader import get_magnetometer, get_rssi
from feature_extractor import extract_features
import csv
import time

label = input("Label (Safe/Suspicious/Threat): ")
num_samples = int(input("How many samples to collect? "))

print(f"\nCollecting {num_samples} samples for {label}...\n")

with open("real_dataset.csv", "a", newline="") as f:
    writer = csv.writer(f)

    for i in range(num_samples):

        readings = []

        for j in range(20):
            readings.append(get_magnetometer())
            time.sleep(0.1)

        features = extract_features(readings, get_rssi())

        writer.writerow([
            features["avg_mag"],
            features["max_mag"],
            features["min_mag"],
            features["variance"],
            features["rssi"],
            label
        ])

        print(
            f"{i+1}/{num_samples} "
            f"AVG={features['avg_mag']:.1f} "
            f"RSSI={features['rssi']}"
        )

        time.sleep(1)

print("\nDone!")
print("Saved to real_dataset.csv")
