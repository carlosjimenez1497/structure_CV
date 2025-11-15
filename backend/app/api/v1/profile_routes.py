from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.models.profile_models import UserProfile, UpdateFromCVRequest
from app.services.profile_service import ProfileService
from app.services.cv_extractor import extract_profile_from_text
from app.utils.pdf_reader import pdf_to_text
from app.core.deps import get_current_user
import tempfile
import json

router = APIRouter()
service = ProfileService()

@router.post("/create")
async def create_profile(
    profile: UserProfile,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a profile for the currently authenticated user.
    Only one profile per user for now.
    """
    try:
        profile_id = service.create(profile, current_user["user_id"])
        return {
            "status": "success",
            "profile_id": profile_id
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/update-from-cv")
async def update_profile_from_cv(
    text_or_json: UpdateFromCVRequest = None,
    file: UploadFile = File(None),
    user=Depends(get_current_user)
):
    """
    Update the user's profile by extracting structured data from:
    - uploaded PDF
    - pasted text
    - pasted JSON
    """

    # --- Get existing profile ---
    profile_id, existing_profile = service.get_profile_by_user(user["user_id"])
    if not existing_profile:
        raise HTTPException(status_code=404, detail="User has no profile")

    # --- Case 1: PDF upload ---
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp.flush()
            extracted_text = pdf_to_text(tmp.name)
            gpt_data = extract_profile_from_text(extracted_text)
            updated = service.update_from_structured_data(user["user_id"], gpt_data)
            return {"status": "success", "profile": updated}

    # --- Case 2: JSON directly ---
    if text_or_json and text_or_json.json_data:
        updated = service.update_from_structured_data(user["user_id"], text_or_json.json_data)
        return {"status": "success", "profile": updated}

    # --- Case 3: Plain text CV ---
    if text_or_json and text_or_json.text:
        gpt_data = extract_profile_from_text(text_or_json.text)
        updated = service.update_from_structured_data(user["user_id"], gpt_data)
        return {"status": "success", "profile": updated}

    raise HTTPException(status_code=400, detail="No valid CV input provided")