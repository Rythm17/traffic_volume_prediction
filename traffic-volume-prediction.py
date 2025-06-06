# -*- coding: utf-8 -*-

# Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Loading the Dataset
traffic_data = pd.read_csv("/content/Metro_Interstate_Traffic_Volume.csv")
traffic_data.head(10)

"""Data Cleaning and Noise Removal"""

# Filling missing 'holiday' with 'None'
traffic_data['holiday'] = traffic_data['holiday'].fillna('None')

# Converting 'date_time' to datetime format
traffic_data['date_time'] = pd.to_datetime(traffic_data['date_time'])
traffic_data.head(10)

"""Feature Engineering: Time - Based Features"""

traffic_data['date_time'] = pd.to_datetime(traffic_data['date_time'])   # (date_time) column - from string to actual datetime format
traffic_data['hour'] = traffic_data['date_time'].dt.hour
traffic_data['dayofweek'] = traffic_data['date_time'].dt.dayofweek
traffic_data.head(10)

# Create a feature for weekend (Saturdays = 5, Sundays = 6)
traffic_data['is_weekend'] = traffic_data['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)  # Flags if a day is Saturday(5) or Sunday(6)
# Create a feature for rush hours (7-9 am, 4-6 pm)
traffic_data['is_rush_hour'] = traffic_data["hour"].apply(lambda x: 1 if x in [7,8,9,16,17,18] else 0)  # Flags whether the time is during rush hours
traffic_data.head(10)

"""Encode Categorical Variable"""

# Convert text weather types (e.g., Clear, Snow) into numerical codes
traffic_data['weather_main'] = traffic_data['weather_main'].astype('category').cat.codes
traffic_data.head(10)

"""Select Features and Target"""

features = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'weather_main', 'hour', 'is_weekend', 'is_rush_hour']
target = 'traffic_volume'
traffic_data.head(10)

"""Box Plot for Outlier Detection"""

plt.figure(figsize = (12, 8))
for i, col in enumerate(features):    #enumerate() helps plot each feature in a grid layout
    plt.subplot(3, 3, i+1)
    sns.boxplot(x = traffic_data[col], color='skyblue')
    plt.title(f"{col} Box Plot", fontsize = 9)
    plt.tight_layout()
plt.suptitle("Box Plots for Outlier Detection", fontsize = 14, y = 1.02)
plt.tight_layout()
plt.show()

# Detect and visualize outliers in target variable
plt.figure(figsize = (8, 4))
sns.boxplot(data = traffic_data, x = 'traffic_volume')
plt.title("Box Plot for Traffic Volume (Outlier Detection)")
plt.show()

# Remove outliers using IQR method
Q1 = traffic_data['traffic_volume'].quantile(0.25)
Q3 = traffic_data['traffic_volume'].quantile(0.75)
IQR = Q3 - Q1
traffic_data = traffic_data[(traffic_data['traffic_volume'] >= Q1 - 1.5 * IQR) & (traffic_data['traffic_volume'] <= Q3 + 1.5 * IQR)]
plt.show()

"""Feature Selection and target + Normalization"""

# Select features and target
features = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'is_weekend', 'is_rush_hour', 'hour', 'dayofweek']
X = traffic_data[features]
y = traffic_data['traffic_volume']

print("Input Features (X): ")
print(X.head(10))

print("\nTarget (y): ")
print(y.head(10))

# Normalize Features using Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_data = pd.DataFrame(X_scaled, columns = X.columns)
print('X_scaled: ')
print(X_scaled_data.head(10))

"""Train - Test Split"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,  random_state = 42)

"""Train Linear Regression Model"""

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

"""Train Random Forest Regressor"""

rf_model = RandomForestRegressor(n_estimators = 100, random_state = 42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Compare Actual vs Predicted (Linear Regression)
print("Linear Regression Predictions vs Actual:\n")
lr_comparison = pd.DataFrame({
    'Actual': y_test.values,
    'Predicted_LR': y_pred_lr
})
print(lr_comparison.head(10))

# Compare Actual vs Predicted (Random Forest Regressor)
print("\n Random Forest Predictions vs Actual:\n")
rf_comparison = pd.DataFrame({
    'Actual': y_test.values,
    'Predicted_rf': y_pred_rf
})
print(rf_comparison.head(10))

"""Evaluation Metrics"""

def print_metrics(y_true, y_pred, model_name):
  print(f"\n {model_name} Performance Metrics:")
  print(f"MAE: {mean_absolute_error(y_true, y_pred): 0.2f}")
  print(f"RMSE: {np.sqrt(mean_squared_error(y_true, y_pred)): 0.2f}")
  print(f"R^2: {r2_score(y_true, y_pred): 0.2f}")

print_metrics(y_test, y_pred_lr, "Linear Regression")
print_metrics(y_test, y_pred_rf, "Random Forest Regressor")

"""Visualization: Actual vs Predicted for both models"""

plt.figure(figsize = (12, 6))
plt.plot(y_test.values[:100], label = 'Actual', marker = 'o')
plt.plot(y_pred_lr[:100], label = 'Linear Regression', marker = 'x')
plt.plot(y_pred_rf[:100], label = 'Random Forest Regressor', marker = 's')
plt.title("Traffic Volume: Actual vs Predicted")
plt.xlabel("Sample Index")
plt.ylabel("Traffic Volume")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()