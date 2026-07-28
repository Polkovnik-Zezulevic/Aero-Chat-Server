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
if os.path.exists(FILE):
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except:
        messages = []
else:
    messages = []

def save_messages():
    """Сохраняем сообщения в файл"""
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.post("/send")
def send(data: dict):
    messages.append({"name": data["name"], "msg": data["msg"]})
    save_messages()  # сохраняем сразу после добавления
    return {"ok": True}

@app.get("/messages")
def get_messages():
    return messages
