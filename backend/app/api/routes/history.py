from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.history_repository import HistoryRepository

router = APIRouter(
    prefix="/history",
    tags=["Interview History"]
)


@router.get("/")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return HistoryRepository.get_all(
        db=db,
        user_id=current_user.id
    )