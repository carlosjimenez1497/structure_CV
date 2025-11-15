from app.models.profile_models import UserProfile
from app.db.fake_db import DB_PROFILES
import uuid

class ProfileService:

    def create(self, profile: UserProfile, user_id: str):
        # Check if the user already has a profile
        for p_id, p_data in DB_PROFILES.items():
            if p_data["user_id"] == user_id:
                raise ValueError("User already has a profile")

        profile_id = str(uuid.uuid4())
        DB_PROFILES[profile_id] = {
            "profile_id": profile_id,
            "user_id": user_id,
            **profile.dict()
        }
        return profile_id

    def get_profile_by_user(self, user_id: str):
        for pid, profile in DB_PROFILES.items():
            if profile["user_id"] == user_id:
                return pid, profile
        return None, None

    def update_from_structured_data(self, user_id: str, new_data: dict):
        pid, profile = self.get_profile_by_user(user_id)
        if not profile:
            raise ValueError("User has no profile")

        # Merge new structured fields (non-destructive)
        updated = copy.deepcopy(profile)
        for key, value in new_data.items():
            if value not in [None, [], ""]:
                updated[key] = value

        DB_PROFILES[pid] = updated
        return updated