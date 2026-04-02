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

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html><body style="font-family:sans-serif;background:#0f0f13;color:#e2e8f0;padding:40px">
    <h1 style="color:#818cf8">CareerPath AI</h1>
    <p>Multi-Agent Career Coach — Google Cloud GenAI Hackathon APAC</p>
    <h3 style="color:#34d399">Status: Live ✓</h3>
    <p><b>Endpoints:</b></p>
    <ul>
      <li>POST /chat — multi-agent chat</li>
      <li>POST /profile — create user profile</li>
      <li>GET /profile/{id} — get wins and goals</li>
      <li>GET /health — health check</li>
    </ul>
    <p><b>Frontend:</b> <a style="color:#818cf8" href="https://careerpath-ai-2026.web.app">https://careerpath-ai-2026.web.app</a></p>
    </body></html>
    """

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

@app.get("/health")
def health():
    return {"status": "ok", "service": "careerpath-ai"}
