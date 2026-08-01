from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession


class InterviewSessionRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        questions: list
    ):

        session = InterviewSession(
            user_id=user_id,
            total_questions=len(questions),
            completed_questions=0,
            overall_score=0,
            questions=questions
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    @staticmethod
    def get_by_id(
        db: Session,
        session_id: int
    ):

        return (
            db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id
            )
            .first()
        )

    @staticmethod
    def update_progress(
        db: Session,
        session: InterviewSession,
        score: int
    ):

        session.completed_questions += 1

        total = session.completed_questions

        session.overall_score = (
            (session.overall_score * (total - 1)) + score
        ) // total

        db.commit()
        db.refresh(session)

        return session