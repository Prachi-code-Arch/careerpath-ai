from pydantic import BaseModel

class Task(BaseModel):
    task_id: str
    user_id: str
    skill: str
    description: str
    week: int
    completed: bool = False

class Win(BaseModel):
    win_id: str
    user_id: str
    title: str
    description: str
    impact_metric: str
    category: str
    used_in_review: bool = False
