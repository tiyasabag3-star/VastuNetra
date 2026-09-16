import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

cols = [
    "AVG_MAG",
    "MAX_MAG",
    "MIN_MAG",
    "MAG_VARIANCE",
    "RSSI",
    "LABEL"
]

df = pd.read_csv(
    "real_dataset.csv",
    names=cols
)

X = df[[
    "AVG_MAG",
    "MAX_MAG",
    "MIN_MAG",
    "MAG_VARIANCE",
    "RSSI"
]]

y = df["LABEL"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("\nClassification Report:\n")
print(classification_report(y_test, pred))

joblib.dump(
    model,
    "../models/airport_threat_model_real.pkl"
)

print("\nModel saved!")
