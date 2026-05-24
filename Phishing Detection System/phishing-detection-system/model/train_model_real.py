import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("=== Phishing Detection Model Training ===")

# Check if sample data exists
if not os.path.exists("sample_phishing_data.csv"):
    print("Error: sample_phishing_data.csv not found!")
    print("Run create_sample_data.py first.")
    exit(1)

# Load data
print("Loading dataset...")
df = pd.read_csv("sample_phishing_data.csv")

# Prepare features and labels
features = ["url_length", "has_ip", "has_at_symbol", "has_dash", "is_https", "subdomain_count"]
X = df[features]
y = df["label"]

print(f"Dataset shape: {X.shape}")
print(f"Features: {features}")
print(f"Classes: {y.value_counts().to_dict()}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print("\nTraining Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nModel Evaluation:")
print(f"Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
print("\nFeature Importance:")
for feature, importance in zip(features, model.feature_importances_):
    print(f"  {feature}: {importance:.3f}")

# Save model
joblib.dump(model, "model/phishing_model.pkl")
print("\n✅ Model saved as \"model/phishing_model.pkl\"")

# Save feature names for reference
with open("model/feature_names.txt", "w") as f:
    for feature in features:
        f.write(f"{feature}\n")
print("✅ Feature names saved")

print("\n=== Training Complete ===")
