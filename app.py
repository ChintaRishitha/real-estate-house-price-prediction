from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import os


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

MODEL_PATH = "model/house_price_model.pkl"
METRICS_PATH = "model/metrics.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

with open(METRICS_PATH, "rb") as file:
    metrics = pickle.load(file)


# --------------------------------------------------
# Available locations
# --------------------------------------------------

locations = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Pune",
    "Delhi",
    "Mumbai",
    "Kolkata"
]


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Model metrics API
# --------------------------------------------------

@app.route("/metrics")
def get_metrics():

    return jsonify({
        "records": metrics["records"],
        "features": metrics["features"],
        "r2": round(metrics["r2"], 4),
        "mae": round(metrics["mae"], 2),
        "rmse": round(metrics["rmse"], 2),
        "locations": locations
    })


# --------------------------------------------------
# Prediction API
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        # Read input values
        area = float(data["area"])
        bedrooms = int(data["bedrooms"])
        bathrooms = int(data["bathrooms"])
        floors = int(data["floors"])
        parking = int(data["parking"])
        age = int(data["age"])
        location = data["location"]

        # --------------------------------------------------
        # Validate inputs
        # --------------------------------------------------

        if not 200 <= area <= 10000:
            return jsonify({
                "error": "Area must be between 200 and 10,000 sq ft."
            }), 400

        if not 1 <= bedrooms <= 6:
            return jsonify({
                "error": "Bedrooms must be between 1 and 6."
            }), 400

        if not 1 <= bathrooms <= 6:
            return jsonify({
                "error": "Bathrooms must be between 1 and 6."
            }), 400

        if not 1 <= floors <= 4:
            return jsonify({
                "error": "Floors must be between 1 and 4."
            }), 400

        if not 0 <= parking <= 4:
            return jsonify({
                "error": "Parking must be between 0 and 4."
            }), 400

        if not 0 <= age <= 50:
            return jsonify({
                "error": "House age must be between 0 and 50 years."
            }), 400

        if location not in locations:
            return jsonify({
                "error": "Please select a valid location."
            }), 400

        # --------------------------------------------------
        # Create input DataFrame
        # --------------------------------------------------

        input_data = pd.DataFrame([{
            "area": area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "floors": floors,
            "parking": parking,
            "age": age,
            "location": location
        }])

        # --------------------------------------------------
        # Make prediction
        # --------------------------------------------------

        prediction = model.predict(input_data)[0]

        # Round prediction to nearest ₹1,000
        prediction = round(prediction / 1000) * 1000

        # --------------------------------------------------
        # Return result
        # --------------------------------------------------

        return jsonify({
            "predicted_price": int(prediction),
            "location": location
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":

    print("----------------------------------------")
    print("Real Estate House Price Prediction System")
    print("----------------------------------------")
    print("Starting Flask server...")
    print("Open: http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )