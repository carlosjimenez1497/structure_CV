from fastapi import APIRouter, HTTPException, Depends
from app.models.user_models import UserRegister, UserLogin
from app.services.auth_service import AuthService
from app.db.engine import get_session

router = APIRouter()
service = AuthService()

@router.post("/register")
async def register(user: UserRegister, session=Depends(get_session)):
    user_id = service.register(user, session)
    return {"user_id": user_id}

@router.post("/login")
async def login(user: UserLogin, session=Depends(get_session)):
    token = service.login(user, session)
    return {"access_token": token}
