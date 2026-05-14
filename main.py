from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from services.db import connect_to_db
from services.websocket import PubSub

load_dotenv()
db = connect_to_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.pubsub = PubSub()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/new-message")
async def new_message(request: Request):
    data = await request.json()
    db["messages"].insert_one(data)
    return {"message": "Message received"}

@app.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    await websocket.accept()
    pubsub = app.state.pubsub
    pubsub.subscribe(topic, websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            await pubsub.publish(topic, msg)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected from topic: {topic}")
        pubsub.unsubscribe(topic, websocket)
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        pubsub.unsubscribe(topic, websocket)