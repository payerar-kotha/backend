from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from services.db import connect_to_db

load_dotenv()
db = connect_to_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/new-message")
async def new_message(request: Request):
    data = await request.json()
    db["messages"].insert_one(data)
    return {"message": "Message received"}