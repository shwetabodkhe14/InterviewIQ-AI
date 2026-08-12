from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.report_repository import ReportRepository
from app.ai.report_generator import ReportGenerator

router = APIRouter(
    prefix="/session",
    tags=["Session Report"]
)

@router.get("/report/{session_id}")
def get_session_report(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session, results = ReportRepository.get_session_and_results(db, session_id, current_user.id)
    
    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found or not authorized."
        )
        
    questions_answered = len(results)
    
    if questions_answered == 0:
        return {
            "candidate": current_user.full_name if hasattr(current_user, 'full_name') and current_user.full_name else current_user.email,
            "session_id": session.id,
            "questions_answered": 0,
            "average_scores": {
                "technical": 0,
                "communication": 0,
                "confidence": 0,
                "grammar": 0,
                "overall": 0
            },
            "strengths": [],
            "weaknesses": [],
            "overall_feedback": "No questions answered.",
            "recommendation": "None"
        }
        
    total_technical = 0
    total_communication = 0
    total_confidence = 0
    total_grammar = 0
    total_overall = 0
    
    strengths_set = set()
    weaknesses_set = set()
    
    for r in results:
        total_technical += r.technical_score or 0
        total_communication += r.communication_score or 0
        total_confidence += r.confidence_score or 0
        total_grammar += r.grammar_score or 0
        total_overall += r.overall_score or 0
        
        if r.strengths:
            for s in r.strengths.split('\n'):
                if s.strip():
                    strengths_set.add(s.strip())
                    
        if r.weaknesses:
            for w in r.weaknesses.split('\n'):
                if w.strip():
                    weaknesses_set.add(w.strip())
                    
    avg_scores = {
        "technical": int((total_technical / questions_answered) * 10),
        "communication": int((total_communication / questions_answered) * 10),
        "confidence": int((total_confidence / questions_answered) * 10),
        "grammar": int((total_grammar / questions_answered) * 10),
        "overall": int((total_overall / questions_answered) * 10)
    }
    
    strengths = list(strengths_set)
    weaknesses = list(weaknesses_set)
    
    # Optional: Take top strengths/weaknesses if the list is too long
    # We will just return all unique for now
    
    ai_feedback = ReportGenerator.generate_overall_feedback(
        technical_score=avg_scores["technical"],
        communication_score=avg_scores["communication"],
        confidence_score=avg_scores["confidence"],
        grammar_score=avg_scores["grammar"],
        strengths=strengths[:10], # Pass top 10 to avoid huge prompt
        weaknesses=weaknesses[:10]
    )
    
    return {
        "candidate": current_user.full_name if hasattr(current_user, 'full_name') and current_user.full_name else current_user.email,
        "session_id": session.id,
        "questions_answered": questions_answered,
        "average_scores": avg_scores,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "overall_feedback": ai_feedback.get("overall_feedback", "N/A"),
        "recommendation": ai_feedback.get("recommendation", "N/A"),
        "coach": {
            "learning_roadmap": ai_feedback.get("learning_roadmap", []),
            "certifications": ai_feedback.get("recommended_certifications", []),
            "technologies": ai_feedback.get("recommended_technologies", []),
            "job_roles": ai_feedback.get("recommended_job_roles", []),
            "companies": ai_feedback.get("recommended_companies", []),
            "next_steps": ai_feedback.get("next_steps", [])
        }
    }
