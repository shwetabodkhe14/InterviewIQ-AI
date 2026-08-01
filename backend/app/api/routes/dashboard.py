from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.repositories.dashboard_repository import DashboardRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    dashboard = DashboardRepository.get_dashboard(
        db,
        current_user.id
    )

    if dashboard is None:
        raise HTTPException(
            status_code=404,
            detail="No interview history found."
        )

    return dashboard