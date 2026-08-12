from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.interview_result import InterviewResult
from app.models.interview_session import InterviewSession
from app.models.resume import Resume


class DashboardRepository:

    @staticmethod
    def get_dashboard(db: Session, user_id: int):

        total = (
            db.query(InterviewSession)
            .filter(InterviewSession.user_id == user_id)
            .count()
        )

        has_resume = (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .first()
        ) is not None

        if total == 0:
            return {
                "total_interviews": 0,
                "average_score": None,
                "highest_score": 0,
                "latest_score": 0,
                "technical_average": 0,
                "communication_average": 0,
                "confidence_average": 0,
                "grammar_average": 0,
                "recent_scores": [],
                "has_resume": has_resume
            }

        average_score = (
            db.query(func.avg(InterviewResult.overall_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        highest_score = (
            db.query(func.max(InterviewResult.overall_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        latest_score = (
            db.query(InterviewResult.overall_score)
            .filter(InterviewResult.user_id == user_id)
            .order_by(InterviewResult.created_at.desc())
            .first()
        )

        technical_avg = (
            db.query(func.avg(InterviewResult.technical_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        communication_avg = (
            db.query(func.avg(InterviewResult.communication_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        confidence_avg = (
            db.query(func.avg(InterviewResult.confidence_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        grammar_avg = (
            db.query(func.avg(InterviewResult.grammar_score))
            .filter(InterviewResult.user_id == user_id)
            .scalar()
        )

        recent_scores = (
            db.query(InterviewResult.overall_score)
            .filter(InterviewResult.user_id == user_id)
            .order_by(InterviewResult.created_at.desc())
            .limit(5)
            .all()
        )

        return {
            "total_interviews": total,
            "average_score": round(average_score or 0, 2),
            "highest_score": highest_score,
            "latest_score": latest_score[0] if latest_score else 0,
            "technical_average": round(technical_avg or 0, 2),
            "communication_average": round(communication_avg or 0, 2),
            "confidence_average": round(confidence_avg or 0, 2),
            "grammar_average": round(grammar_avg or 0, 2),
            "recent_scores": [score[0] for score in recent_scores],
            "has_resume": has_resume
        }