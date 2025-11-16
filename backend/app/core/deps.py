from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select
from app.db.engine import get_session
from app.db.models import User
from app.core.auth import decode_access_token

auth_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    session=Depends(get_session)
):
    token = credentials.credentials
    
    try:
        payload = decode_access_token(token)
        user_id = payload["sub"]

        user = session.exec(select(User).where(User.user_id == user_id)).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
