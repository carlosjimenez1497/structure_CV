from sqlmodel import select
from fastapi import Depends, HTTPException
from app.db.engine import get_session
from app.db.models import User
from app.core.auth import hash_password, verify_password, create_access_token

class AuthService:

    def register(self, data, session):
        existing = session.exec(select(User).where(User.email == data.email)).first()
        if existing:
            raise ValueError("Username already exists")

        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            full_name=data.full_name
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user.user_id

    def login(self, data, session):
        user = session.exec(select(User).where(User.email == data.email)).first()
        if not user:
            raise ValueError("User not found")

        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid password")

        return create_access_token(user.user_id)
