from modules.database import chat_history
from datetime import datetime

def save_chat(user_id, question, answer):

    chat_history.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "created_at": datetime.now()
    })