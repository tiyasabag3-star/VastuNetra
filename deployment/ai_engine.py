import joblib
import pandas as pd

# =====================================
# Load Trained Model
# =====================================
MODEL_PATH = "/home/vastunetra/vastunetra-main/vastunetra-main/deployment/airport_threat_model_v2.pkl"

model = joblib.load(MODEL_PATH)

# =====================================
# Prediction Function
# =====================================
def predict_threat(features):
    """
    Predict object from extracted features.
    """

    # Convert dictionary to DataFrame
    X = pd.DataFrame([features])

    # Arrange columns exactly as used during training
    X = X[model.feature_names_in_]

    # Predict
    prediction = model.predict(X)[0]

    # Confidence
    confidence = max(model.predict_proba(X)[0]) * 100

    return prediction, confidence


# =====================================
# Test
# =====================================
if __name__ == "__main__":

    from sensor_reader_v2 import get_all_sensors, get_rssi
    from feature_extractor_v2 import extract_features

    sensors = get_all_sensors()
    features = extract_features(sensors, get_rssi())

    print("\nFeatures:")
    for k, v in features.items():
        print(f"{k:20}: {v}")

    prediction, confidence = predict_threat(features)

    print("\nPrediction :", prediction)
    print("Confidence :", round(confidence, 2), "%")
