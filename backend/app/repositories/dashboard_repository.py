from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.interview_result import InterviewResult


class DashboardRepository:

    @staticmethod
    def get_dashboard(db: Session, user_id: int):

        total = (
            db.query(InterviewResult)
            .filter(InterviewResult.user_id == user_id)
            .count()
        )

        if total == 0:
            return None

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
            "average_score": round(average_score, 2),
            "highest_score": highest_score,
            "latest_score": latest_score[0] if latest_score else 0,
            "technical_average": round(technical_avg, 2),
            "communication_average": round(communication_avg, 2),
            "confidence_average": round(confidence_avg, 2),
            "grammar_average": round(grammar_avg, 2),
            "recent_scores": [score[0] for score in recent_scores]
        }