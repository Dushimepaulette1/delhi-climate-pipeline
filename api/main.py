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