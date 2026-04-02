from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

def save_user_profile(user_id: str, profile: dict):
    db.collection("users").document(user_id).set(profile, merge=True)

def get_user_profile(user_id: str) -> dict:
    doc = db.collection("users").document(user_id).get()
    return doc.to_dict() if doc.exists else {}

def save_win(user_id: str, win: dict):
    win["date"] = datetime.utcnow().isoformat()
    db.collection("users").document(user_id)\
      .collection("wins").document(win["win_id"]).set(win)

def get_wins(user_id: str) -> list:
    docs = db.collection("users").document(user_id)\
             .collection("wins").stream()
    return [d.to_dict() for d in docs]

def save_goal(user_id: str, goal: dict):
    goal["created_at"] = datetime.utcnow().isoformat()
    db.collection("users").document(user_id)\
      .collection("goals").document(goal["goal_id"]).set(goal)

def get_goals(user_id: str) -> list:
    docs = db.collection("users").document(user_id)\
             .collection("goals").stream()
    return [d.to_dict() for d in docs]

def save_session_message(user_id: str, session_id: str, role: str, content: str, agent: str):
    db.collection("users").document(user_id)\
      .collection("sessions").document(session_id)\
      .set({
          "messages": firestore.ArrayUnion([{
              "role": role,
              "content": content,
              "agent": agent,
              "ts": datetime.utcnow().isoformat()
          }])
      }, merge=True)

def log_agent_action(user_id: str, session_id: str, agent: str, action: str, result: str):
    db.collection("users").document(user_id)\
      .collection("sessions").document(session_id)\
      .set({
          "agent_log": firestore.ArrayUnion([{
              "agent": agent,
              "action": action,
              "result": result,
              "ts": datetime.utcnow().isoformat()
          }])
      }, merge=True)
