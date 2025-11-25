from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserAccount(BaseModel):
    user_id: str
    username: str
    password_hash: str