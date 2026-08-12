from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.session_answer import SessionAnswerRequest, InterviewStartRequest
from app.ai.answer_evaluator import AnswerEvaluator
from app.ai.gemini_parser import GeminiParser
from app.ai.interview_generator import InterviewGenerator
from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.parser.resume_parser import ResumeParser
from app.repositories.interview_session_repository import InterviewSessionRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.interview_result_repository import (
    InterviewResultRepository
)

router = APIRouter(
    prefix="/session",
    tags=["Interview Session"]
)


@router.post("/start")
def start_interview(
    request: InterviewStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Get latest uploaded resume
    resume = ResumeRepository.get_latest_resume(
        db,
        current_user.id
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found."
        )

    # Extract resume text
    text = ResumeParser.extract_text(
        resume.filepath
    )

    # Parse using Gemini
    resume_data = GeminiParser.extract_resume_data(
        text
    )

    # Generate interview questions
    questions_dict = InterviewGenerator.generate_questions(
        resume_data,
        company=request.company,
        difficulty=request.difficulty,
        domain=request.domain
    )

    questions = []
    if questions_dict:
        questions.extend(questions_dict.get("hr", []))
        questions.extend(questions_dict.get("technical", []))
        questions.extend(questions_dict.get("projects", []))

    if len(questions) == 0:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate interview questions."
        )

    # Create interview session
    session = InterviewSessionRepository.create(
    db=db,
    user_id=current_user.id,
    questions=questions
)

    return {
        "session_id": session.id,
        "question_number": 1,
        "total_questions": len(questions),
        "question": questions[0]
    }
@router.post("/answer")
def answer_question(
    request: SessionAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    session = InterviewSessionRepository.get_by_id(
        db,
        request.session_id
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Unauthorized session."
        )

    current_index = session.completed_questions

    if not session.questions:
        raise HTTPException(
            status_code=500,
            detail="No questions are available for this session. Please start a new session."
        )

    if current_index >= len(session.questions):
        return {
            "message": "Interview already completed."
        }

    question = session.questions[current_index]

    from google.genai.errors import ClientError
    try:
        result = AnswerEvaluator.evaluate(
            question=question,
            answer=request.answer
        )
    except ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            raise HTTPException(
                status_code=429,
                detail="AI service rate limit exceeded. Please wait about 30-60 seconds before trying again."
            )
        raise HTTPException(
            status_code=500,
            detail="An error occurred while evaluating your answer with the AI."
        )

    InterviewResultRepository.create(
        db=db,
        user_id=current_user.id,
        question=question,
        answer=request.answer,
        evaluation=result,
        session_id=session.id
    )

    InterviewSessionRepository.update_progress(
        db=db,
        session=session,
        score=result["overall_score"]
    )

    if session.completed_questions >= len(session.questions):

        return {
            "completed": True,
            "overall_score": session.overall_score
        }

    next_question = session.questions[
        session.completed_questions
    ]

    return {
        "completed": False,
        "question_number": session.completed_questions + 1,
        "question": next_question,
        "overall_score": session.overall_score,
        "evaluation": result
    }