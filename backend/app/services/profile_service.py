from app.models.profile_models import UserProfile
from app.db.store import add_profile, get_profile_by_user_id, update_profile

class ProfileService:
    def create(self, profile: UserProfile, user_id: str):
        pid, existing = get_profile_by_user_id(user_id)
        if existing:
            raise ValueError("User already has a profile")

        profile_id = add_profile({
            "user_id": user_id,
            **profile.dict(),
        })
        return profile_id

    def get_by_user(self, user_id: str):
        return get_profile_by_user_id(user_id)

    def update_from_structured_data(self, user_id: str, data: dict):
        pid, existing = get_profile_by_user_id(user_id)
        if not existing:
            raise ValueError("User has no profile")

        merged = {**existing}
        for k, v in data.items():
            if v not in [None, "", [], {}]:
                merged[k] = v

        return update_profile(pid, merged)
