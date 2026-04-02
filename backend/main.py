from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from agents.orchestrator import run as orchestrate
from tools.firestore_tool import save_user_profile, get_wins, get_goals
from models.user_profile import UserProfile

app = FastAPI(title="CareerPath AI", version="1.0")

@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return JSONResponse({}, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        })
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    result = orchestrate(req.user_id, req.message, req.session_id)
    return result

@app.post("/profile")
def create_profile(profile: UserProfile):
    save_user_profile(profile.user_id, profile.dict())
    return {"status": "profile saved", "user_id": profile.user_id}

@app.get("/profile/{user_id}")
def get_profile_data(user_id: str):
    wins = get_wins(user_id)
    goals = get_goals(user_id)
    return {"user_id": user_id, "wins": wins, "goals": goals}
