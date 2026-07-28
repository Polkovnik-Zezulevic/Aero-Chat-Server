import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FILE = "messages.json"

# Загружаем сообщения из файла при запуске
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = []

# Функция сохранения
def save_messages():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.post("/send")
def send(data: dict):
    messages.append({"name": data["name"], "msg": data["msg"]})
    save_messages()  # сохраняем каждый раз
    return {"ok": True}

@app.get("/messages")
def get_messages():
    return messages
