from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ConflictError
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token


class AuthService:
    """Authentication service."""

    @staticmethod
    def register(db: Session, user_data: UserRegister) -> User:
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ConflictError(f"User with email {user_data.email} already exists")

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(email=user_data.email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, credentials: UserLogin) -> Token:
        """Authenticate user and return access token."""
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")

