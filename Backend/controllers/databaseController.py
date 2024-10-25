import os
import dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi import HTTPException

dotenv.load_dotenv()

client: Optional[AsyncIOMotorClient] = None

async def connect_to_database():
    global client
    if client is None:
        try:
            mongo_uri = os.getenv("MONGO")
            if not mongo_uri:
                raise ValueError("MongoDB URI not found in environment variables.")
            client = AsyncIOMotorClient(mongo_uri)
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise HTTPException(status_code=500, detail="Database connection error")

async def close_database_connection():
    global client
    if client is not None:
        client.close()
        client = None
        print("MongoDB connection closed")

async def get_users_collection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.users
    return db.get_collection("users")

async def get_project_collection():
    if client is None:
        raise HTTPException(status_code=500, detail="Database connection not established")
    db = client.projects
    return db.get_collection("projectDetails")
