import joblib
import pandas as pd

MODEL_PATH = "/home/roshan/AirportThreatDetection/models/airport_threat_model_real.pkl"

model = joblib.load(MODEL_PATH)

def predict_threat(features):

    X = pd.DataFrame([{
        "AVG_MAG": features["avg_mag"],
        "MAX_MAG": features["max_mag"],
        "MIN_MAG": features["min_mag"],
        "MAG_VARIANCE": features["variance"],
        "RSSI": features["rssi"]
    }])

    prediction = model.predict(X)[0]

    confidence = max(model.predict_proba(X)[0]) * 100

    return prediction, confidence
