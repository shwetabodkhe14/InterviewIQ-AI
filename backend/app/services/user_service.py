from app.core.security import create_access_token
from app.security.password import (
    hash_password,
    verify_password
)
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
    @staticmethod
    def login_user(db: Session, email: str, password: str):

        user = UserRepository.get_user_by_email(db, email)

        if not user:
            raise ValueError("Invalid email or password.")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        access_token = create_access_token(
            {
                "sub": user.email
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }    