from sqlalchemy.orm import Session

from app.models.interview_result import InterviewResult


class HistoryRepository:

    @staticmethod
    def get_all(db: Session, user_id: int):

        results = (
            db.query(InterviewResult)
            .filter(InterviewResult.user_id == user_id)
            .order_by(InterviewResult.created_at.desc())
            .all()
        )

        history = []

        for item in results:
            history.append({
                "id": item.id,
                "question": item.question,
                "overall_score": item.overall_score,
                "technical_score": item.technical_score,
                "communication_score": item.communication_score,
                "confidence_score": item.confidence_score,
                "grammar_score": item.grammar_score,
                "feedback": item.feedback,
                "strengths": item.strengths,
                "weaknesses": item.weaknesses,
                "created_at": item.created_at
            })

        return history