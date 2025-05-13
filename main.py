from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class PingRequest(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    message: str

    class Config:
        allow_population_by_field_name = True

class WakeRequest(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    reason: str

    class Config:
        allow_population_by_field_name = True

@app.get("/")
def read_root():
    return {"message": "Agent Ping Test is Live!"}

@app.post("/agent-ping")
def agent_ping(request: PingRequest):
    response = {
        "echo": request.message,
        "status": "pong",
        "from": request.from_,
        "to": request.to,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        httpx.post("https://kai-relay.onrender.com/agent-ping", json=response)
    except Exception as e:
        print(f"[ERROR] Forwarding ping to Kai failed: {e}")

    return response

@app.post("/agent-wake")
def agent_wake(request: WakeRequest):
    response = {
        "acknowledged": True,
        "status": "awake",
        "received_from": request.from_,
        "to": request.to,
        "reason": request.reason,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        httpx.post("https://kai-relay.onrender.com/agent-wake", json=response)
    except Exception as e:
        print(f"[ERROR] Forwarding wake to Kai failed: {e}")

    return response
