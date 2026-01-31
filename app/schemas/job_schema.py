from pydantic import BaseModel, Field
from typing import List, Optional

class JobExperienceRequirement(BaseModel):
    role: str
    required_years: Optional[int]

class JobSchema(BaseModel):
    title: str
    company: str
    required_skills: List[str]
    nice_to_have_skills: List[str] = []
    experience_requirements: List[JobExperienceRequirement]
    education_level: Optional[str]
    keywords: List[str] = []

class JobRequest(BaseModel):
    job_description: str = Field(..., max_length=15000)
