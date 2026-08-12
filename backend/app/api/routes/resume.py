from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post(
    "/upload",
    response_model=ResumeResponse
)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from google.genai.errors import ClientError
    try:
        return ResumeService.upload_resume(
            db=db,
            file=file,
            user_id=current_user.id
        )
    except ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            raise HTTPException(
                status_code=429,
                detail="AI service rate limit exceeded. Please wait about 30-60 seconds before uploading your resume."
            )
        raise HTTPException(
            status_code=500,
            detail="An error occurred with the AI service while parsing your resume."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )