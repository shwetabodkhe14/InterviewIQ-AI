from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai.gemini_parser import GeminiParser
from app.ai.interview_generator import InterviewGenerator
from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.parser.resume_parser import ResumeParser
from app.repositories.resume_repository import ResumeRepository

router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


@router.post("/generate")
def generate_interview_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = ResumeRepository.get_latest_resume(
        db,
        current_user.id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    text = ResumeParser.extract_text(
        resume.filepath
    )

    resume_data = GeminiParser.extract_resume_data(
        text
    )

    questions = InterviewGenerator.generate_questions(
        resume_data
    )

    return questions