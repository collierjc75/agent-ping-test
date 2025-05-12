from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pytz

app = FastAPI()

class PingRequest(BaseModel):
    from_: str
    to: str
    message: str

class PingResponse(BaseModel):
    from_: str
    to: str
    echo: str
    status: str = "pong"

class WakeRequest(BaseModel):
    from_: str
    target: str
    reason: str

class WakeResponse(BaseModel):
    acknowledged: bool = True
    status: str = "awake"
    received_from: str
    timestamp: str

@app.post("/agent-ping-test", response_model=PingResponse)
async def agent_ping(payload: PingRequest):
    return PingResponse(from_=payload.from_, to=payload.to, echo=payload.message)

@app.post("/agent-wake", response_model=WakeResponse)
async def agent_wake(payload: WakeRequest):
    return WakeResponse(
        received_from=payload.from_,
        timestamp=datetime.now(pytz.utc).isoformat()
    )
