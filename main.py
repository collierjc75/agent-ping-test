from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class WakeRequest(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    reason: str

    class Config:
        allow_population_by_field_name = True

@app.get("/")
def home():
    return {"message": "Agent Ping Test is Live!"}

@app.get("/agent-ping")
def ping():
    return {"status": "ok", "message": "ping received"}

@app.post("/agent-wake")
def wake(request: WakeRequest):
    return {
        "acknowledged": True,
        "status": "awake",
        "received_from": request.from_,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
