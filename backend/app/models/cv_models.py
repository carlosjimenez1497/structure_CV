# backend/app/models/cv_models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Experience(BaseModel):
    role: str
    company: str
    description: Optional[str]
    start_date: str
    end_date: Optional[str]

class Education(BaseModel):
    degree: str
    institution: str
    year: str

class CVInput(BaseModel):
    name: str
    title: Optional[str]
    summary: Optional[str]
    skills: List[str]
    experience: List[Experience]
    education: List[Education]


class Section(BaseModel):
    title: str
    body_md: str = Field(..., description="Markdown content for the section")

class CVGenerated(BaseModel):
    name: str
    title: Optional[str]
    sections: List[Section]
    skills: List[str]
    latex: Optional[str] = None


class CVTargetRequest(BaseModel):
    profile_id: int
    job_description: str
