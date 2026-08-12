from sqlalchemy.orm import Session

from app.models.interview_result import InterviewResult

class InterviewResultRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        question: str,
        answer: str,
        evaluation: dict,
        session_id: int = None
    ):

        result = InterviewResult(
            user_id=user_id,
            session_id=session_id,
            question=question,
            answer=answer,
            technical_score=evaluation["technical_score"],
            communication_score=evaluation["communication_score"],
            confidence_score=evaluation["confidence_score"],
            grammar_score=evaluation["grammar_score"],
            overall_score=evaluation["overall_score"],
            strengths="\n".join(evaluation["strengths"]),
            weaknesses="\n".join(evaluation["weaknesses"]),
            feedback=evaluation["feedback"]
        )

        db.add(result)
        db.commit()
        db.refresh(result)

        return result