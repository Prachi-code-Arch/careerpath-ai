from tools.gemini_tool import call_gemini
from tools.firestore_tool import save_session_message
from config import GEMINI_FLASH
import json

def run(user_message: str, user_profile: dict) -> dict:
    user_id = user_profile.get("user_id", "unknown")

    prompt = f"""
You are a career schedule planner for a {user_profile.get('role', 'professional')}
in {user_profile.get('city', 'India')} at {user_profile.get('company', 'a company')}.

User message: "{user_message}"

Create a specific weekly schedule to help them achieve their career goal.
Include: review prep sessions, skill-building blocks, networking time.
Be specific with days, times, and durations.

Respond ONLY in JSON:
{{
  "events": [
    {{
      "title": "",
      "day": "",
      "time": "",
      "duration_mins": 0,
      "reason": "",
      "google_calendar_link": ""
    }}
  ],
  "weekly_summary": "",
  "total_hours_per_week": 0
}}
"""
    result = call_gemini(prompt, model=GEMINI_FLASH)

    try:
        clean = result.strip().replace("```json", "").replace("```", "")
        parsed = json.loads(clean)
        for event in parsed.get("events", []):
            title = event.get("title", "Career Task")
            day = event.get("day", "Monday")
            time = event.get("time", "9:00 AM")
            duration = event.get("duration_mins", 60)
            event["google_calendar_link"] = (
                f"https://calendar.google.com/calendar/render"
                f"?action=TEMPLATE"
                f"&text={title.replace(' ', '+')}"
                f"&details=CareerPath+AI+scheduled+session"
                f"&duration={duration}"
            )
        result = json.dumps(parsed)
    except:
        pass

    return {"agent": "schedule_agent", "output": result}
