from app.database.base import Base
from app.database.connection import engine

# Import all models here
from app.models.user import User


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables created successfully!")


if __name__ == "__main__":
    create_tables()