from app.database.base import Base
from app.database.connection import engine

# Import every model so SQLAlchemy registers them
from app.models.user import User
from app.models.resume import Resume
from app.models.interview_result import InterviewResult


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully!")


if __name__ == "__main__":
    create_tables()