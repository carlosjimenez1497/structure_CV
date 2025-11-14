from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.auth import decode_access_token
from app.db.fake_db import DB_USERS

auth_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = payload["sub"]
        if user_id not in DB_USERS:
            raise ValueError("User not found")
        return DB_USERS[user_id]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
