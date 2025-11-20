from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models.profile_models import UserProfile, UserProfileUpdate, UpdateFromCVRequest
from app.services.profile_service import ProfileService
from app.core.deps import get_current_user
from app.db.engine import get_session

router = APIRouter()
service = ProfileService()

@router.post("/create")
async def create_profile(
    profile: UserProfile,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        profile_id = service.create(current_user.user_id, profile, session)
        return {"status": "success", "profile_id": profile_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update")
async def update_profile_manually(
    updates: UserProfileUpdate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        updated = service.update_manual(current_user.user_id, updates, session)
        return {"status": "success", "profile": updated}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
