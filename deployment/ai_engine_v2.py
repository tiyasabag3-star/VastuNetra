import joblib
import pandas as pd

# ==============================
# Load Trained Model
# ==============================
model = joblib.load("airport_threat_model_v2.pkl")


def predict_object(features):
    """
    Predict object from extracted features.

    Returns:
        prediction (str)
        confidence (float)
    """

    # Convert features to DataFrame
    df = pd.DataFrame([features])

    # Predict probabilities
    probs = model.predict_proba(df)[0]
    classes = model.classes_

    # Get best prediction
    best_idx = probs.argmax()
    prediction = classes[best_idx]
    confidence = probs[best_idx] * 100

    # Print all probabilities
    print("\n==============================")
    print("CLASS PROBABILITIES")
    print("==============================")

    sorted_probs = sorted(
        zip(classes, probs),
        key=lambda x: x[1],
        reverse=True
    )

    for cls, prob in sorted_probs:
        print(f"{cls:<12} : {prob*100:.2f}%")

    print("==============================")

    # Confidence threshold
    if confidence < 47:
        prediction = "unknown"

    return prediction, confidence


# ==============================
# Test
# ==============================
if __name__ == "__main__":

    from sensor_reader_v2 import get_all_sensors, get_rssi
    from feature_extractor_v2 import extract_features

    sensors = get_all_sensors()

    features = extract_features(
        sensors,
        get_rssi()
    )

    prediction, confidence = predict_object(features)

    print("\nPrediction :", prediction)
    print(f"Confidence : {confidence:.2f}%")
