from sqlalchemy.orm import Session
from app.models.interview_session import InterviewSession
from app.models.interview_result import InterviewResult

class ReportRepository:
    
    @staticmethod
    def get_session_and_results(db: Session, session_id: int, user_id: int):
        session = db.query(InterviewSession).filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_id
        ).first()
        
        if not session:
            return None, None
            
        results = db.query(InterviewResult).filter(
            InterviewResult.session_id == session.id
        ).all()
        
        return session, results
