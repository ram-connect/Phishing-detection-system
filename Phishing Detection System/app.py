from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from utils.feature_extractor import extract_features

app = Flask(__name__)

# Load model
model = None
try:
    model = joblib.load("model/phishing_model.pkl")
    print("✅ Machine Learning Model loaded successfully")
    print("   Running in ML mode")
except Exception as e:
    model = None
    print("⚠️  Model not found - running in heuristic mode")
    print(f"   Error: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_url():
    url = request.form.get("url", "").strip()
    
    if not url:
        return jsonify({"error": "No URL provided"})
    
    # Extract features
    features_dict = extract_features(url)
    
    # Convert to DataFrame for model prediction
    features_df = pd.DataFrame([features_dict])
    
    # Ensure we have the right features in the right order
    required_features = ["url_length", "has_ip", "has_at_symbol", 
                         "has_dash", "is_https", "subdomain_count"]
    
    # Add missing features with default values
    for feature in required_features:
        if feature not in features_df.columns:
            features_df[feature] = 0
    
    # Reorder columns
    features_df = features_df[required_features]
    
    # Make prediction
    if model is not None:
        try:
            prediction = model.predict(features_df)[0]
            result = "🚨 PHISHING" if prediction == 1 else "✅ SAFE"
            
            # Get confidence score
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(features_df)[0]
                confidence = proba[1] if prediction == 1 else proba[0]
            else:
                confidence = 0.85 if prediction == 1 else 0.15
        except Exception as e:
            print(f"Prediction error: {e}")
            result = "⚠️  ERROR in ML prediction"
            confidence = 0.5
    else:
        # Heuristic mode
        if features_dict.get("has_ip", False) or features_dict.get("has_at_symbol", False):
            result = "⚠️  SUSPICIOUS (Heuristic)"
            confidence = 0.7
        elif features_dict.get("has_dash", False) and features_dict.get("subdomain_count", 0) > 2:
            result = "⚠️  SUSPICIOUS (Heuristic)"
            confidence = 0.6
        else:
            result = "✅ LIKELY SAFE (Heuristic)"
            confidence = 0.3
    
    return jsonify({
        "url": url,
        "result": result,
        "confidence": float(confidence),
        "features": features_dict,
        "mode": "ML" if model is not None else "Heuristic"
    })

@app.route("/api/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "mode": "ML" if model is not None else "Heuristic"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Changed to port 5001 to avoid conflict
