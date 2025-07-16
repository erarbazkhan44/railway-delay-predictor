import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import os

# Set page config
st.set_page_config(page_title="Railway Delay Predictor", layout="centered")

st.title("🚆 Railway Delay Prediction")
st.write("Predict train delay in real-time using a Machine Learning model.")

# === Load Model Safely ===
MODEL_PATH = "model/delay_predictor.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file not found. Please train the model first using `train_model.py`.")
    st.stop()

model = joblib.load(MODEL_PATH)

# === Input UI ===
stations = ['Delhi', 'Mumbai', 'Chennai', 'Pune', 'Hyderabad']  # Must match training

train_no = st.text_input("Enter Train Number", "12345")
station = st.selectbox("Select Station", stations)
scheduled_time = st.time_input("Scheduled Departure Time")

# === Predict Button ===
if st.button("Predict Delay"):
    try:
        # Process input
        hour = scheduled_time.hour
        input_data = pd.DataFrame({
            'train_no': [int(train_no)],
            'scheduled_hour': [hour],
            **{f'station_{s}': [1 if s == station else 0] for s in stations}
        })

        # Align columns with model training
        model_features = model.feature_names_in_
        for col in model_features:
            if col not in input_data.columns:
                input_data[col] = 0  # Add missing dummy station columns
        input_data = input_data[model_features]  # Ensure correct order

        # Predict
        prediction = model.predict(input_data)[0]
        st.success(f"🚦 Expected Delay: **{int(prediction)} minutes**")

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {str(e)}")
