from app.database.base import Base
from app.database.connection import engine

# Import ALL models
from app.models.user import User
from app.models.resume import Resume
from app.models.interview_result import InterviewResult

Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")