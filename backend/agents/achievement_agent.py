from tools.gemini_tool import call_gemini
from tools.firestore_tool import save_win, get_wins
from config import GEMINI_FLASH
import json, uuid

def run(user_message: str, user_profile: dict) -> dict:
    user_id = user_profile.get("user_id", "unknown")

    past_wins = get_wins(user_id)
    wins_context = f"Past wins logged: {len(past_wins)}" if past_wins else "No wins logged yet."

    prompt = f"""
You are a career achievement tracker helping a {user_profile.get('role', 'professional')}
at {user_profile.get('company', 'a company')} in {user_profile.get('city', 'India')}.

User said: "{user_message}"
{wins_context}

Extract any wins or achievements and convert them into strong performance
review bullet points with impact metrics.
If no wins mentioned, ask one specific question to uncover a recent achievement.

Respond ONLY in JSON:
{{
  "wins_found": [
    {{"title": "", "bullet_point": "", "impact_metric": "", "category": ""}}
  ],
  "follow_up_question": ""
}}
"""
    result = call_gemini(prompt, model=GEMINI_FLASH)

    try:
        clean = result.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(clean)
        for win in parsed.get("wins_found", []):
            if win.get("title"):
                save_win(user_id, {
                    "win_id": str(uuid.uuid4()),
                    "title": win["title"],
                    "bullet_point": win.get("bullet_point", ""),
                    "impact_metric": win.get("impact_metric", ""),
                    "category": win.get("category", "delivery"),
                    "used_in_review": False
                })
    except:
        pass

    return {"agent": "achievement_agent", "output": result}
