from sensor_reader import get_magnetometer, get_rssi
from feature_extractor import extract_features
import time

samples = []

print("Collecting samples...")

for i in range(20):
    samples.append(get_magnetometer())
    time.sleep(0.1)

features = extract_features(
    samples,
    get_rssi()
)

print("\nExtracted Features:")
print(features)
