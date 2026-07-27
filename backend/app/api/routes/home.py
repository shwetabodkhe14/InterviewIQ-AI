from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to InterviewIQ AI 🚀",
        "status": "Backend is running successfully!"
    }