from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

from config import ATLAS_URI, DB_NAME
from src.main import create_app

app = create_app()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()