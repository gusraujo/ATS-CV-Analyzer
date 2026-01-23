from pydantic import BaseModel, Field
from typing import List


class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    start_month: str = ""
    start_year: str = ""
    end_month: str = ""
    end_year: str = ""
    description: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    field: str = ""
    start_month: str = ""
    start_year: str = ""
    end_month: str = ""
    end_year: str = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)


class CV(BaseModel):
    personal_info: PersonalInfo = PersonalInfo()
    summary: str = ""
    skills: dict = Field(default_factory=lambda: {
        "technical": [],
        "soft": []
    })
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
