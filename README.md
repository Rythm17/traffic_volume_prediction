# 🚗 Traffic Volume Prediction

This project leverages machine learning techniques to predict hourly traffic volume based on various temporal and weather-related features. By analyzing historical data, it aims to assist in traffic management and urban planning.

## 📊 Dataset

The model is trained on the Metro Interstate Traffic Volume dataset from the UCI Machine Learning Repository. This dataset contains hourly traffic volume data alongside weather and time information.

## 🛠️ Features

*Temporal Features*: Hour, day of the week, month, holiday indicators.

*Weather Features*: Temperature, rain, snow, cloud cover, weather description.

## 🧠 Models Used

*Linear Regression*: A baseline model to establish initial performance metrics.

*Random Forest Regressor*: An ensemble model that improves prediction accuracy by averaging multiple decision trees.

## 🗂️ Project Structure

```bash
traffic_volume_prediction/
├── streamlit_app.py           # Main application script
├── traffic_volume_prediction.py # Model training and evaluation
├── traffic_lr_model.pkl         # Saved Linear Regression model
├── traffic_rf_model.pkl         # Saved Random Forest model
├── traffic_scaler.pkl           # Scaler for feature normalization
├── requirements.txt             # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.x installed. Install the required packages using:

```bash
pip install -r requirements.txt
```

### Running the Application

Execute the main script to start the prediction application:

```bash
streamlit run streamlit_app.py
```

This will launch a Streamlit web application where you can input feature values and obtain traffic volume predictions.

## 📈 Model Performance

The Random Forest model outperforms the Linear Regression model, achieving higher accuracy and better generalization on unseen data. Performance metrics include Mean Absolute Error (MAE), Mean Squared Error (MSE), and R-squared (R²) score.



