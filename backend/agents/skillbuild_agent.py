from tools.gemini_tool import call_gemini
from tools.firestore_tool import save_goal, get_goals
from config import GEMINI_FLASH
import json, uuid

def run(user_message: str, user_profile: dict) -> dict:
    user_id = user_profile.get("user_id", "unknown")

    past_goals = get_goals(user_id)
    goals_context = f"Active goals: {len(past_goals)}" if past_goals else "No goals set yet."

    prompt = f"""
You are a skill development coach for a {user_profile.get('role', 'professional')}
with {user_profile.get('years_exp', 2)} years experience in {user_profile.get('city', 'India')}.

User message: "{user_message}"
{goals_context}

Identify skill gaps and create a focused 4-week micro-task plan (30-60 mins/day).

Respond ONLY in JSON:
{{
  "skill_identified": "",
  "four_week_plan": [
    {{"week": 1, "focus": "", "daily_task": "", "time_required": ""}}
  ],
  "first_task_today": ""
}}
"""
    result = call_gemini(prompt, model=GEMINI_FLASH)

    try:
        clean = result.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(clean)
        if parsed.get("skill_identified"):
            save_goal(user_id, {
                "goal_id": str(uuid.uuid4()),
                "skill": parsed["skill_identified"],
                "weekly_tasks": parsed.get("four_week_plan", []),
                "status": "active",
                "progress_pct": 0
            })
    except:
        pass

    return {"agent": "skillbuild_agent", "output": result}
