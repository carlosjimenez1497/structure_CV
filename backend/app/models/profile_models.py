from pydantic import BaseModel, Field
from typing import List, Optional


# -------------------------------
# EXPERIENCE SECTION
# -------------------------------
class Experience(BaseModel):
    role: str = Field(..., description="Job title or role")
    company: str = Field(..., description="Company name")
    description: Optional[str] = Field(
        None, description="Detailed job responsibilities or achievements"
    )
    start_date: str = Field(..., description="YYYY-MM or YYYY")
    end_date: Optional[str] = Field(None, description="YYYY-MM or YYYY, or None if ongoing")


# -------------------------------
# EDUCATION SECTION
# -------------------------------
class Education(BaseModel):
    degree: str = Field(..., description="Academic degree or program")
    institution: str = Field(..., description="Name of the institution")
    year: str = Field(..., description="Year of graduation")


# -------------------------------
# OPTIONAL LIKE PROJECTS (nice for future CV)
# -------------------------------
class Project(BaseModel):
    name: str
    description: Optional[str] = None
    tech_stack: List[str] = []


# -------------------------------
# MAIN PROFILE MODEL
# -------------------------------
class UserProfile(BaseModel):
    name: str = Field(..., description="Full name of the user")
    title: Optional[str] = Field(None, description="Professional headline")
    summary: Optional[str] = Field(None, description="Short professional summary")

    skills: List[str] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)


# -------------------------------
# PARTIAL UPDATE MODEL (PATCH)
# -------------------------------
class UserProfileUpdate(BaseModel):
    """
    For update_profile_manually endpoint
    All fields optional so UI can patch only changed sections.
    """
    name: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None

    skills: Optional[List[str]] = None

    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    projects: Optional[List[Project]] = None



class UpdateFromCVRequest(BaseModel):
    text: Optional[str] = None
    json_data: Optional[dict] = None
