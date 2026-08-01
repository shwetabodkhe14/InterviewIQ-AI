from pydantic import BaseModel


class SessionAnswerRequest(BaseModel):
    session_id: int
    answer: str