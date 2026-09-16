import numpy as np

def extract_features(sensor_data, rssi):
    features = {}
    mags = []

    # -----------------------------
    # Read all four sensors
    # -----------------------------
    for i in range(1, 5):

        sensor = sensor_data.get(f"sensor{i}", {})

        x = sensor.get("x", 0)
        y = sensor.get("y", 0)
        z = sensor.get("z", 0)
        mag = sensor.get("magnitude", 0)

        # Replace None with 0
        x = 0 if x is None else x
        y = 0 if y is None else y
        z = 0 if z is None else z
        mag = 0 if mag is None else mag

        features[f"mag_{i}"] = float(mag)
        features[f"x_{i}"] = float(x)
        features[f"y_{i}"] = float(y)
        features[f"z_{i}"] = float(z)

        mags.append(float(mag))

    mags = np.array(mags, dtype=float)

    # -----------------------------
    # Global Statistics
    # -----------------------------
    features["avg_mag"] = float(np.mean(mags))
    features["max_mag"] = float(np.max(mags))
    features["min_mag"] = float(np.min(mags))
    features["range_mag"] = float(np.max(mags) - np.min(mags))
    features["std_mag"] = float(np.std(mags))

    # -----------------------------
    # Spatial Features
    # -----------------------------
    left = (mags[0] + mags[2]) / 2
    right = (mags[1] + mags[3]) / 2

    top = (mags[0] + mags[1]) / 2
    bottom = (mags[2] + mags[3]) / 2

    features["left_right_diff"] = float(left - right)
    features["top_bottom_diff"] = float(top - bottom)
    features["diag1_diff"] = float(mags[0] - mags[3])
    features["diag2_diff"] = float(mags[1] - mags[2])

    # -----------------------------
    # Extra Pairwise Differences
    # -----------------------------
    features["diff_12"] = float(abs(mags[0] - mags[1]))
    features["diff_13"] = float(abs(mags[0] - mags[2]))
    features["diff_14"] = float(abs(mags[0] - mags[3]))
    features["diff_23"] = float(abs(mags[1] - mags[2]))
    features["diff_24"] = float(abs(mags[1] - mags[3]))
    features["diff_34"] = float(abs(mags[2] - mags[3]))

    # -----------------------------
    # Normalized Magnitudes
    # -----------------------------
    total = np.sum(mags)

    if total == 0:
        total = 1

    features["norm_mag_1"] = float(mags[0] / total)
    features["norm_mag_2"] = float(mags[1] / total)
    features["norm_mag_3"] = float(mags[2] / total)
    features["norm_mag_4"] = float(mags[3] / total)

    # -----------------------------
    # Strongest Sensor
    # -----------------------------
    features["strongest_sensor"] = int(np.argmax(mags) + 1)

    # -----------------------------
    # RSSI
    # -----------------------------
    features["rssi"] = int(rssi)

    return features


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    from sensor_reader_v2 import get_all_sensors, get_rssi

    sensors = get_all_sensors()

    features = extract_features(
        sensors,
        get_rssi()
    )

    print("\nExtracted Features\n")
    print("-" * 50)

    for key, value in features.items():
        print(f"{key:20}: {value}")
