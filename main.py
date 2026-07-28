from fastapi import FastAPI, WebSocket
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

# Загружаем старые сообщения
if os.path.exists(FILE):
    with open(FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = []

def save_messages():
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# Список активных клиентов
clients = []

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)
    # Отправляем историю при подключении
    await ws.send_json(messages)
    try:
        while True:
            data = await ws.receive_json()
            messages.append(data)
            save_messages()
            # Рассылаем всем
            for client in clients:
                await client.send_json(messages)
    except:
        clients.remove(ws)

@app.get("/messages")
def get_messages():
    return messages
