from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []

@app.post("/send")
def send(data: dict):
    messages.append({"name": data["name"], "msg": data["msg"]})
    return {"ok": True}

@app.get("/messages")
def get_messages():
    return messages
