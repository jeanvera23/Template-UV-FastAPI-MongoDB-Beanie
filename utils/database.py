from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.UsersModel import UsersModel

import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "my_database")

client = None
db = None

async def connectToDatabase():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    await init_beanie(database=db, document_models=[UsersModel])
    print("✅ Connected to MongoDB database:", DB_NAME)

async def closeDatabaseConnection():
    global client
    if client:
        client.close()
        print("🚪 MongoDB connection closed")