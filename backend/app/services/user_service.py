from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.security.password import hash_password


class UserService:

    @staticmethod
    def register_user(db: Session, user_data: UserCreate):

        existing_user = UserRepository.get_user_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError("Email already registered.")

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )

        return UserRepository.create_user(db, new_user)