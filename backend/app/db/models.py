from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid

class User(SQLModel, table=True):
    user_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True, index=True
    )
    username: str = Field(index=True, unique=True)
    password_hash: str

    # relationship
    profile: Optional["Profile"] = Relationship(back_populates="user")


class Profile(SQLModel, table=True):
    profile_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True, index=True
    )
    user_id: str = Field(foreign_key="user.user_id")
    
    name: str
    title: Optional[str] = None
    summary: Optional[str] = None
    
    skills: str = ""  # store comma-separated or JSON string
    experience: str = ""  # JSON string
    education: str = ""  # JSON string
    projects: str = ""  # JSON string

    user: Optional[User] = Relationship(back_populates="profile")
