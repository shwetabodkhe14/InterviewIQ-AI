from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.resume import router as resume_router
from app.api.routes.interview import router as interview_router
from app.api.routes.evaluation import router as evaluation_router
app = FastAPI(
    title="InterviewIQ AI",
    version="1.0.0"
)

# ==========================
# Register API Routers
# ==========================

# Authentication APIs
app.include_router(auth_router)

# Resume APIs
app.include_router(resume_router)

# Interview APIs
app.include_router(interview_router)

app.include_router(evaluation_router)
# ==========================
# Root Endpoint
# ==========================

@app.get("/")
def root():
    return {
        "message": "InterviewIQ AI Backend Running 🚀"
    }