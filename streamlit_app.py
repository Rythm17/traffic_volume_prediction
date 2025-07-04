# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import joblib

# Load saved models and scaler
@st.cache_resource
def load_models():
    try:
        lr_model = joblib.load("traffic_lr_model.pkl")
        rf_model = joblib.load("traffic_rf_model.pkl")
        scaler = joblib.load("traffic_scaler.pkl")
        return lr_model, rf_model, scaler
    except Exception as e:
        st.error(f"❌ Failed to load model files: {e}")
        st.stop()

lr_model, rf_model, scaler = load_models()

# Streamlit app setup
st.set_page_config(page_title = "Traffic Volume Predictor", layout = "centered")
st.title("🚦 Traffic Volume Prediction")
st.markdown("Enter the conditions to predict estimated traffic volume.")

# ---- Input features ----
temp = st.number_input("Temperature (in Kelvin)", min_value = 250.0, max_value = 330.0, value = 293.0)
rain_1h = st.number_input("Rainfall in last 1 hour (mm)", min_value = 0.0, max_value = 50.0, value = 0.0)
snow_1h = st.number_input("Snowfall in last 1 hour (mm)", min_value = 0.0, max_value = 50.0, value = 0.0)
clouds_all = st.slider("Cloud Cover (%)", min_value = 0, max_value = 100, value = 40)
weather_main = st.selectbox("Weather Condition",
 ["Clear", "Clouds", "Drizzle", "Fog", "Haze", "Mist", "Rain",
 "Smoke", "Snow", "Squall", "Thunderstorm", "Other"
])
weather_map = {
    "Clear": 0, "Clouds": 1, "Drizzle": 2, "Fog": 3, "Haze": 4,
    "Mist": 5, "Rain": 6, "Smoke": 7, "Snow": 8, "Squall": 9,
    "Thunderstorm": 10, "Other": 11
}
weather_code = weather_map[weather_main]

hour = st.slider("Hour of the Day", min_value = 0, max_value = 23, value = 14)
dayofweek = st.selectbox("Day of the Week", [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])
dow_map = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
    "Friday": 4, "Saturday": 5, "Sunday": 6
}
dayofweek_code = dow_map[dayofweek]

# ---- Derived Features ----
is_weekend = 1 if dayofweek_code >= 5 else 0
is_rush_hour = 1 if hour in [7,8,9,16,17,18] else 0

import pandas as pd
# --- Define the feature order as in training ---
feature_names = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'is_weekend', 'is_rush_hour', 'hour', 'dayofweek']

# --- Create DataFrame ---
features_df = pd.DataFrame([[temp, rain_1h, snow_1h, clouds_all, is_weekend, is_rush_hour, hour, dayofweek_code]],columns=feature_names)

# --- Scale input ---
scaled_features = scaler.transform(features_df)

# --- Predict on button click ---
if st.button("Predict traffic volume"):
  pred_lr = int(lr_model.predict(features_df)[0])
  pred_rf = int(rf_model.predict(features_df)[0])

  st.subheader("Prediction Results")
  st.success(f"**Linear Regression Prediction:** {pred_lr} vehicles")
  st.success(f"**Random Forest Prediction:** {pred_rf} vehicles")

  st.markdown("These results are based on your input conditions using two trained models.")
