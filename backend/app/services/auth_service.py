from app.models.user_models import UserRegister, UserLogin
from app.core.auth import hash_password, verify_password, create_access_token
from app.db.fake_db import DB_USERS
import uuid

class AuthService:

    def register(self, data: UserRegister):
        # Check if username taken
        for user in DB_USERS.values():
            if user["username"] == data.username:
                raise ValueError("Username already exists")
        
        user_id = str(uuid.uuid4())
        DB_USERS[user_id] = {
            "user_id": user_id,
            "username": data.username,
            "password_hash": hash_password(data.password)
        }
        return user_id

    def login(self, data: UserLogin):
        # Find user
        for user in DB_USERS.values():
            if user["username"] == data.username:
                if verify_password(data.password, user["password_hash"]):
                    token = create_access_token(user["user_id"])
                    return token
                raise ValueError("Invalid password")
        raise ValueError("User not found")
