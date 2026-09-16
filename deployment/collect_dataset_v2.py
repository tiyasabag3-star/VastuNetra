import csv
import os

from sensor_reader_v2 import get_all_sensors, get_rssi
from feature_extractor_v2 import extract_features

# ==================================
# Dataset File
# ==================================
DATASET_FILE = "dataset_v2.csv"

# ==================================
# Create Dataset with Header
# ==================================
if not os.path.exists(DATASET_FILE):

    print("Creating dataset file...")

    while True:
        try:
            features = extract_features(get_all_sensors(), get_rssi())

            with open(DATASET_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                headers = list(features.keys())
                headers.append("label")
                writer.writerow(headers)

            print("Dataset created successfully.")
            break

        except Exception:
            print("Waiting for sensors...")
            continue

# ==================================
# User Input
# ==================================
print("=" * 50)
print("      AIRPORT AI DATA COLLECTION V2")
print("=" * 50)

label = input("\nEnter Object Label : ").strip().lower()
samples = int(input("Number of Samples : "))

print("\nMove the object before every capture.")
print("Press ENTER to capture each sample.\n")

# ==================================
# Collect Dataset
# ==================================
saved = 0

while saved < samples:

    input(f"Sample {saved + 1}/{samples} -> Press ENTER")

    try:

        sensors = get_all_sensors()
        rssi = get_rssi()

        features = extract_features(sensors, rssi)

        row = list(features.values())
        row.append(label)

        with open(DATASET_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        saved += 1

        print(f"✓ Sample {saved}/{samples} Saved")

    except Exception as e:

        print("⚠ Error while reading sensors.")
        print(e)
        print("Retrying...")

# ==================================
# Finished
# ==================================
print("\n" + "=" * 50)
print("Dataset collection completed successfully!")
print(f"Total samples collected: {saved}")
print(f"Saved to: {DATASET_FILE}")
print("=" * 50)
