from sqlmodel import select
from fastapi import HTTPException
from app.db.models import Profile
from app.utils.serializers import dumps_json, loads_json

class ProfileService:

    def create(self, user_id: str, profile_data, session):
        # Check if the user already has a profile
        existing = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if existing:
            raise ValueError("User already has a profile")

        profile = Profile(
            user_id=user_id,
            name=profile_data.name,
            title=profile_data.title,
            summary=profile_data.summary,
            skills=dumps_json(profile_data.skills),
            experience=dumps_json([exp.dict() for exp in profile_data.experience]),
            education=dumps_json([edu.dict() for edu in profile_data.education]),
            projects=dumps_json([proj.dict() for proj in profile_data.projects])
        )

        session.add(profile)
        session.commit()
        session.refresh(profile)

        return profile.profile_id

    def get_by_user(self, user_id: str, session):
        profile = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
        return profile

    def update_manual(self, user_id: str, updates, session):
        profile = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise ValueError("User has no profile")

        update_data = updates.dict(exclude_unset=True)

        # Apply updates dynamically
        for field, value in update_data.items():
            if field in ["skills", "experience", "education", "projects"]:
                setattr(profile, field, dumps_json(value))
            else:
                setattr(profile, field, value)

        session.add(profile)
        session.commit()
        session.refresh(profile)

        return profile

    def update_structured(self, user_id: str, new_data: dict, session):
        profile = session.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise ValueError("User has no profile")

        for key, value in new_data.items():
            if value not in [None, "", [], {}]:
                if key in ["skills", "experience", "education", "projects"]:
                    setattr(profile, key, dumps_json(value))
                else:
                    setattr(profile, key, value)

        session.add(profile)
        session.commit()
        session.refresh(profile)

        return profile
