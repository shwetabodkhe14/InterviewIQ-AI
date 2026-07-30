from sqlalchemy.orm import Session

from app.models.resume import Resume


class ResumeRepository:

    @staticmethod
    def create(
        db: Session,
        filename: str,
        filepath: str,
        user_id: int
    ):

        resume = Resume(
            filename=filename,
            filepath=filepath,
            user_id=user_id
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume

    @staticmethod
    def get_latest_resume(
        db: Session,
        user_id: int
    ):

        return (
            db.query(Resume)
            .filter(
                Resume.user_id == user_id
            )
            .order_by(
                Resume.uploaded_at.desc()
            )
            .first()
        )