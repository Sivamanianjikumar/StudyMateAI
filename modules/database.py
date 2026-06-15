from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))

db = client["studymate"]
users = db["users"]
chat_history = db["chat_history"]
generated_content = db["generated_content"]