from pydantic import BaseModel
from typing import List, Optional

class JobExperienceRequirement(BaseModel):
    role: str
    required_years: Optional[int]

class JobSchema(BaseModel):
    title: str
    company: str
    required_skills: List[str]
    nice_to_have_skills: Optional[List[str]] = []
    experience_requirements: List[JobExperienceRequirement]
    education_level: Optional[str]  # ex: "Bachelor", "Master"
    keywords: Optional[List[str]] = []
