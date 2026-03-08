mport pickle
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
