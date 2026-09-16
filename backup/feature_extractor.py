import numpy as np

def extract_features(samples, rssi):

    magnitudes = [s["magnitude"] for s in samples]

    features = {
        "avg_mag": float(np.mean(magnitudes)),
        "max_mag": float(np.max(magnitudes)),
        "min_mag": float(np.min(magnitudes)),
        "variance": float(np.var(magnitudes)),
        "delta": float(np.max(magnitudes) - np.min(magnitudes)),
        "rssi": rssi
    }

    return features
