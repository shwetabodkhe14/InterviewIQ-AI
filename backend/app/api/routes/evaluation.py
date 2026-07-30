from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.answer_evaluator import AnswerEvaluator
from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.interview_result_repository import InterviewResultRepository

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)


@router.post("/")
def evaluate_answer(
    question: str,
    answer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    result = AnswerEvaluator.evaluate(
        question,
        answer
    )

    InterviewResultRepository.create(
        db=db,
        user_id=current_user.id,
        question=question,
        answer=answer,
        evaluation=result
    )

    return result