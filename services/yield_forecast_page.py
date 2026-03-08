import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib
import tensorflow as tf
from datetime import datetime
from services.smart_diary import save_yield_history

BASE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Yield_Forecast",
    "models",
    "saved_models"
)
BASE_DIR = os.path.abspath(BASE_DIR)

# ------------------ MODEL LOADING FUNCTION ------------------
def load_crop_model(crop_name):
    crop = crop_name.lower()

    model_file = os.path.join(BASE_DIR, f"{crop}_lstm_model.h5")
    scaler_file = os.path.join(BASE_DIR, f"{crop}_scaler.pkl")

    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model not found: {model_file}")
    if not os.path.exists(scaler_file):
        raise FileNotFoundError(f"Scaler not found: {scaler_file}")

    model = tf.keras.models.load_model(model_file, compile=False)
    scaler = joblib.load(scaler_file)

    # Automatically detect features
    config = {"timesteps": 1, "features": scaler.n_features_in_}

    return model, scaler, config


# ---------------- YIELD FORECAST PAGE -------------------
def yield_forecast_page():
    st.title("🌾 Crop Yield Forecast")
    st.write("Predict crop yield using environment and soil features.")

    crops_available = [
        "Banana", "chickpea", "Cotton", "Groundnut", "Corn", "Rice",
        "Wheat", "Maize", "Sugarcane", "Tomato", "Potato",
        "turmeric", "soybean", "sunflower", "mustard",
        "orange", "onion", "mango"
    ]

    # ------------------ SINGLE PREDICTION ------------------
    st.subheader("Forecast yield for one crop")

    crop_name = st.selectbox("Crop", crops_available)

    try:
        model, scaler, config = load_crop_model(crop_name)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return

    temperature = st.number_input("Temperature (°C)", 0.0, 60.0, 25.0)
    rainfall = st.number_input("Rainfall (mm)", 0.0, 2000.0, 800.0)
    humidity = st.number_input("Humidity (%)", 0.0, 100.0, 60.0)
    nitrogen = st.number_input("Soil Nitrogen", 0.0, 300.0, 150.0)
    soil_ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)

    prediction = None  # Initialize to avoid UnboundLocalError

    if st.button("🔍 Predict Yield"):
        try:
            input_data = np.array([[temperature, rainfall, humidity, nitrogen, soil_ph]])
            scaled = scaler.transform(input_data)
            reshaped = scaled.reshape((1, config["timesteps"], config["features"]))

            prediction = model.predict(reshaped)[0][0]
            st.success(f"✅ Estimated Yield: **{prediction:.2f} tons/hectare**")

            # ✅ Save yield history after successful prediction
            save_yield_history({
                "date": datetime.now(),
                "crop_name": crop_name,
                "region": "default",
                "year": datetime.now().year,
                "temperature": temperature,
                "rainfall": rainfall,
                "humidity": humidity,
                "soil_nitrogen": nitrogen,
                "soil_ph": soil_ph,
                "predicted_yield": float(prediction)
            })
            st.info("📦 Record saved in yield history!")

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    yield_forecast_page()
