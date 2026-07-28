from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE = "messages.json"

# Загружаем сообщения при старте
def load_messages():
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            f.write("[]")
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        # если файл битый — пересоздаём
        with open(FILE, "w", encoding="utf-8") as f:
            f.write("[]")
        return []

messages = load_messages()

def save_messages():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.post("/send")
def send(data: dict):
    messages.append({"name": data["name"], "msg": data["msg"]})
    save_messages()
    return {"ok": True}

@app.get("/messages")
def get_messages():
    return messages
