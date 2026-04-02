from pydantic import BaseModel
from typing import Optional

class UserProfile(BaseModel):
    user_id: str
    name: str
    role: str
    company: str
    city: str
    years_exp: int
    review_date: Optional[str] = None
    salary: Optional[int] = None
    target_salary: Optional[int] = None
    mentor: bool = False
    first_gen: bool = True
