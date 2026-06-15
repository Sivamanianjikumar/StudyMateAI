from pymongo import MongoClient
from dotenv import load_dotenv
import os

print("Step 1: Starting...")

load_dotenv()
print("Step 2: Env loaded")

uri = os.getenv("MONGO_URI")
print("Step 3: URI =", uri)

client = MongoClient(uri, serverSelectionTimeoutMS=5000)

print("Step 4: Trying ping...")

try:
    client.admin.command("ping")
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ Failed:", e)