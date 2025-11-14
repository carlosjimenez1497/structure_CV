from fastapi import APIRouter, HTTPException
from app.models.user_models import UserRegister, UserLogin
from app.services.auth_service import AuthService

router = APIRouter()
service = AuthService()

@router.post("/register")
async def register(user: UserRegister):
    try:
        user_id = service.register(user)
        return {"status": "success", "user_id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    try:
        token = service.login(user)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
