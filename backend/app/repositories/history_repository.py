from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession

class HistoryRepository:

    @staticmethod
    def get_all(db: Session, user_id: int):

        results = (
            db.query(InterviewSession)
            .filter(InterviewSession.user_id == user_id)
            .order_by(InterviewSession.created_at.desc())
            .all()
        )

        history = []

        for item in results:
            history.append({
                "id": item.id,
                "overall_score": item.overall_score,
                "completed_questions": item.completed_questions,
                "total_questions": item.total_questions,
                "created_at": item.created_at
            })

        return history