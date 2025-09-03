# src/db.py

from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB connection URI securely
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise Exception("MongoDB connection string not found. Set MONGO_URI in your .env file.")

# Initialize the MongoDB client and connect to 'telecom_db' database
client = MongoClient(MONGO_URI)
db = client.telecom_db

# Reference to the users collection
users_col = db.users
