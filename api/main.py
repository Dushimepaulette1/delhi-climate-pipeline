import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymysql
from pymongo import MongoClient

app = FastAPI(title="Agri-Predict Climate API")

# DATABASE CONNECTIONS

def get_mysql_connection():
    return pymysql.connect(
        host='localhost',
        user='paulette_api',
        password='AgriPredict123!',
        database='assignment_db',
        cursorclass=pymysql.cursors.DictCursor
    )

MONGO_URI = "mongodb+srv://dushime:Dushimepaulette@cluster0.gbi3qsl.mongodb.net/assignment_db?retryWrites=true&w=majority"
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["assignment_db"]
mongo_collection = mongo_db["climate_records"]

# DATA MODELS

class ClimateRecord(BaseModel):
    record_date: str
    mean_temp: float
    humidity: float
    wind_speed: float
    station_id: int

class WeatherInput(BaseModel):
    month: int
    day_of_year: int
    day_of_week: int
    humidity: float
    wind_speed: float
    meanpressure: float
    lag_1d: float
    lag_7d: float
    lag_30d: float
    ma_7d: float
    ma_30d: float

# TASK 4: LOAD THE RANDOM FOREST MODEL
try:
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Random Forest Champion Model loaded successfully!")
except Exception as e:
    print(f"Model not found: {e}")
    model = None

# API ENDPOINTS (CRUD & PREDICT)

@app.get("/")
def home():
    return {"message": "Welcome to the Agri-Predict API"}

# MySQL ENDPOINTS (CRUD + Time Series)

@app.post("/api/mysql/records")
def add_mysql_record(record: ClimateRecord):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO Daily_Climate (record_date, mean_temp, humidity, wind_speed, station_id)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (record.record_date, record.mean_temp, record.humidity, record.wind_speed, record.station_id))
            connection.commit()
            return {"message": "Record added successfully to MySQL!"}
    finally:
        connection.close()

@app.get("/api/mysql/records")
def get_mysql_records():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Daily_Climate")
            records = cursor.fetchall()
            for r in records:
                r['record_date'] = str(r['record_date'])
            return records
    finally:
        connection.close()

@app.put("/api/mysql/records/{date}")
def update_mysql_record(date: str, record: ClimateRecord):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = """UPDATE Daily_Climate
                     SET mean_temp=%s, humidity=%s, wind_speed=%s, station_id=%s
                     WHERE record_date=%s"""
            cursor.execute(sql, (record.mean_temp, record.humidity, record.wind_speed, record.station_id, date))
            connection.commit()
            return {"message": f"Record for {date} updated successfully in MySQL!"}
    finally:
        connection.close()

@app.delete("/api/mysql/records/{date}")
def delete_mysql_record(date: str):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM Daily_Climate WHERE record_date=%s"
            cursor.execute(sql, (date,))
            connection.commit()
            return {"message": f"Record for {date} deleted successfully from MySQL!"}
    finally:
        connection.close()

@app.get("/api/mysql/latest")
def get_mysql_latest():
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Daily_Climate ORDER BY record_date DESC LIMIT 1")
            record = cursor.fetchone()
            if record:
                record['record_date'] = str(record['record_date'])
            return record
    finally:
        connection.close()

@app.get("/api/mysql/range")
def get_mysql_range(start_date: str, end_date: str):
    connection = get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Daily_Climate WHERE record_date BETWEEN %s AND %s ORDER BY record_date"
            cursor.execute(sql, (start_date, end_date))
            records = cursor.fetchall()
            for r in records:
                r['record_date'] = str(r['record_date'])
            return records
    finally:
        connection.close()

# MongoDB ENDPOINTS (CRUD + Time Series)

@app.post("/api/mongodb/records")
def add_mongo_record(record: dict):
    mongo_collection.insert_one(record)
    return {"message": "Record added successfully to MongoDB!"}

@app.get("/api/mongodb/records")
def get_mongo_records():
    records = list(mongo_collection.find({}, {"_id": 0}))
    return records

@app.put("/api/mongodb/records/{date}")
def update_mongo_record(date: str, record: dict):
    record.pop("_id", None) # Remove ID if present to prevent MongoDB immutable errors
    mongo_collection.update_one({"date": date}, {"$set": record})
    return {"message": f"Record for {date} updated successfully in MongoDB!"}

@app.delete("/api/mongodb/records/{date}")
def delete_mongo_record(date: str):
    mongo_collection.delete_one({"date": date})
    return {"message": f"Record for {date} deleted successfully from MongoDB!"}

@app.get("/api/mongodb/latest")
def get_mongo_latest():
    # Sort by date descending and limit to 1
    record = mongo_collection.find_one({}, sort=[("date", -1)], projection={"_id": 0})
    return record

@app.get("/api/mongodb/range")
def get_mongo_range(start_date: str, end_date: str):
    records = list(mongo_collection.find(
        {"date": {"$gte": start_date, "$lte": end_date}},
        {"_id": 0}
    ).sort("date", 1))
    return records

# PREDICTION ENDPOINT (TASK 4)

@app.post("/api/predict")
def predict_tomorrow(data: WeatherInput):
    if model is None:
        raise HTTPException(status_code=500, detail="AI Model is not loaded. Check if best_model.pkl is in the directory.")

    # Convert incoming JSON into a Pandas DataFrame
    input_data = pd.DataFrame([data.model_dump()])

    # Ensure exact column order for the model
    features = ['month', 'day_of_year', 'day_of_week', 'humidity', 'wind_speed', 'meanpressure',
                'lag_1d', 'lag_7d', 'lag_30d', 'ma_7d', 'ma_30d']
    input_data = input_data[features]

    # Make prediction
    prediction = model.predict(input_data)

    return {
        "message": "Prediction successful",
        "predicted_tomorrow_temp": round(float(prediction[0]), 2),
        "model_used": "RandomForestRegressor"
    }
