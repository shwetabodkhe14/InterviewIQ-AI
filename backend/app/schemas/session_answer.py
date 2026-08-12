from pydantic import BaseModel


class SessionAnswerRequest(BaseModel):
    session_id: int
    answer: str

class InterviewStartRequest(BaseModel):
    company: str | None = None
    difficulty: str | None = None
    domain: str | None = None