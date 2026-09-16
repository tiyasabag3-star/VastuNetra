import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

# =====================================
# Load Dataset
# =====================================
DATASET = "dataset_v2.csv"

df = pd.read_csv(DATASET)

print("Dataset Shape:", df.shape)

# =====================================
# Features and Labels
# =====================================
X = df.drop(columns=["label"])
y = df["label"]

print("\nClasses:")
print(y.value_counts())

# =====================================
# Train/Test Split
# =====================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
    shuffle=True
)

# =====================================
# Train Model
# =====================================
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# =====================================
# Evaluate Model
# =====================================
y_pred = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# =====================================
# Feature Importance
# =====================================
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 15 Important Features:\n")
print(importance.head(15))

# =====================================
# Save Model
# =====================================
MODEL_NAME = "airport_threat_model_v2.pkl"

joblib.dump(model, MODEL_NAME)

print(f"\nModel saved as {MODEL_NAME}")
