import uuid
from app.db.json_db import load_db, save_db

def get_db():
    return load_db()


# ---------------------------
# USERS
# ---------------------------

def add_user(user_data):
    db = load_db()
    user_id = str(uuid.uuid4())

    db["users"][user_id] = {**user_data, "user_id": user_id}
    save_db(db)
    return user_id


def get_user_by_username(username: str):
    db = load_db()
    for user in db["users"].values():
        if user["username"] == username:
            return user
    return None


def get_user_by_id(user_id: str):
    db = load_db()
    return db["users"].get(user_id)


# ---------------------------
# PROFILES
# ---------------------------

def add_profile(profile_data):
    db = load_db()
    profile_id = str(uuid.uuid4())

    db["profiles"][profile_id] = {
        "profile_id": profile_id,
        **profile_data
    }
    save_db(db)
    return profile_id


def update_profile(profile_id: str, updated_profile):
    db = load_db()
    db["profiles"][profile_id] = updated_profile
    save_db(db)
    return updated_profile


def get_profile_by_user_id(user_id: str):
    db = load_db()
    for pid, profile in db["profiles"].items():
        if profile["user_id"] == user_id:
            return pid, profile
    return None, None
