from pydantic import BaseModel
from typing import Literal, Optional, Dict


class Observation(BaseModel):
    comment: str
    user_history: Dict
    post_topic: str
    toxicity_score: float
    step_count: int


class Action(BaseModel):
    action_type: Literal[
        "allow",
        "delete",
        "flag",
        "respond",
        "warn",
        "ban"
    ]
    response_text: Optional[str] = None


class Reward(BaseModel):
    score: float
    reason: str


class State(BaseModel):
    comments_handled: int
    toxicity_level: float
    engagement_score: float
    banned_users: int
    step_count: int