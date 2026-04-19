from tools.gemini_tool import call_gemini
from tools.firestore_tool import get_user_profile, save_session_message, log_agent_action, get_wins, get_goals
from agents import schedule_agent, achievement_agent, skillbuild_agent, coach_agent
from config import GEMINI_PRO
import json, uuid

ROUTING_PROMPT = """
You are a career manager AI. Based on the user message, decide which agents to call.
Agents:
- schedule_agent: calendar, meetings, booking time, review prep dates, scheduling
- achievement_agent: wins, accomplishments, performance review, what I did
- skillbuild_agent: learning, skills, improving, being weak at something, want to get better
- coach_agent: advice, salary, promotion, difficult conversations, what should I do
User message: "{message}"
Respond ONLY with a JSON array. Example: ["coach_agent", "achievement_agent"]
Always include coach_agent for general career questions.
"""

def route(user_message: str) -> list:
    prompt = ROUTING_PROMPT.format(message=user_message)
    response = call_gemini(prompt, model=GEMINI_PRO, temperature=0.1)
    try:
        clean = response.strip().replace("```json", "").replace("```", "")
        return json.loads(clean)
    except:
        return ["coach_agent"]

def run(user_id: str, user_message: str, session_id: str = None) -> dict:
    if not session_id:
        session_id = str(uuid.uuid4())
    user_profile = get_user_profile(user_id)
    if not user_profile:
        user_profile = {
            "name": "User", "role": "Professional",
            "company": "Their Company", "city": "Delhi",
            "years_exp": 2, "first_gen": True, "mentor": False
        }
    user_profile["user_id"] = user_id
    wins = get_wins(user_id)
    goals = get_goals(user_id)
    user_profile["total_wins"] = len(wins)
    user_profile["active_goals"] = len(goals)
    save_session_message(user_id, session_id, "user", user_message, "user")
    agents_to_call = route(user_message)
    agent_results = []
    activity_log = []
    AGENT_MAP = {
        "schedule_agent": schedule_agent,
        "achievement_agent": achievement_agent,
        "skillbuild_agent": skillbuild_agent,
        "coach_agent": coach_agent,
    }
    for agent_name in agents_to_call:
        if agent_name in AGENT_MAP:
            result = AGENT_MAP[agent_name].run(user_message, user_profile)
            agent_results.append(result)
            activity_log.append({
                "agent": agent_name,
                "status": "completed",
                "preview": str(result["output"])[:100]
            })
            log_agent_action(user_id, session_id, agent_name, "ran", str(result["output"])[:200])
    synthesis_prompt = f"""
You are CareerPath AI, a career coach for first-generation professionals in APAC.
User: {user_profile.get('name')} | Role: {user_profile.get('role')} | Company: {user_profile.get('company')}
Wins logged so far: {user_profile.get('total_wins', 0)} | Active goals: {user_profile.get('active_goals', 0)}
User asked: "{user_message}"
Your specialist agents found:
{json.dumps(agent_results, indent=2)}
Combine into ONE clear, warm, practical response. Be specific to their situation.
End with one concrete action they can take today.
"""
    final_response = call_gemini(synthesis_prompt, model=GEMINI_PRO, temperature=0.6)
    save_session_message(user_id, session_id, "assistant", final_response, "orchestrator")
    return {
        "session_id": session_id,
        "response": final_response,
        "agents_called": agents_to_call,
        "activity_log": activity_log,
        "user_context": {
            "wins_logged": user_profile.get("total_wins", 0),
            "active_goals": user_profile.get("active_goals", 0)
        }
    }
