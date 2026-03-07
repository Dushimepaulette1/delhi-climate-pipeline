import requests
import pandas as pd
import pickle
import datetime

print("  DELHI DAILY TEMPERATURE FORECAST PIPELINE")

# STEP 1: LOAD MODEL
print("[Step 1] Loading model artifacts...")
try:
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("  Model: RandomForestRegressor loaded successfully.")
except Exception as e:
    print(f"  Error loading model: {e}")
    exit()

# STEP 2: FETCH LATEST DATA FROM API
print("[Step 2] Fetching the latest record from API...")
try:
    # We hit our own API to get the latest MySQL record!
    response = requests.get("http://127.0.0.1:8000/api/mysql/latest")
    latest_data = response.json()
    record_date = latest_data.get("record_date", "2013-01-04")
    print(f"  Latest date in DB: {record_date} | temp={latest_data.get('mean_temp')}C")
except Exception as e:
    print(f"  Warning: Could not reach API. Is it running? Error: {e}")
    # Fallback mock data if server is off
    record_date = "2013-01-04"
    latest_data = {"humidity": 71.33, "wind_speed": 1.23}

# STEP 3: PREPROCESS DATA 
print("[Step 3] Preprocessing features for model input...")
# Convert string date to datetime object to extract month and day features
date_obj = datetime.datetime.strptime(record_date, "%Y-%m-%d")
forecast_date = date_obj + datetime.timedelta(days=1)

# Assemble the 11 exact features the Random Forest requires
# (Using actual fetched data where available, and filling moving averages/lags for the example)
features_dict = {
    "month": forecast_date.month,
    "day_of_year": forecast_date.timetuple().tm_yday,
    "day_of_week": forecast_date.weekday(),
    "humidity": latest_data.get("humidity", 65.0),
    "wind_speed": latest_data.get("wind_speed", 12.5),
    "meanpressure": 1005.0, # Filled default as this wasn't in original MySQL schema
    "lag_1d": latest_data.get("mean_temp", 29.5),
    "lag_7d": 28.0, 
    "lag_30d": 25.0,
    "ma_7d": 28.5,
    "ma_30d": 26.2
}

input_df = pd.DataFrame([features_dict])
print(f"  Feature shape: {input_df.shape} | forecast_date: {forecast_date.strftime('%Y-%m-%d')}")

# --- STEP 4: GENERATE FORECAST ---
print("[Step 4] Generating forecast...")
prediction = model.predict(input_df)
predicted_temp = round(float(prediction[0]), 2)

print(f"  FORECAST ({forecast_date.strftime('%Y-%m-%d')}): {predicted_temp} C")
