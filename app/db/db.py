import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import certifi





load_dotenv()
connection=os.getenv("mongo_uri")
client=AsyncIOMotorClient(connection,tlsCAFile=certifi.where())
db=client.task_db
tasks=db.task_collection
users=db.users
