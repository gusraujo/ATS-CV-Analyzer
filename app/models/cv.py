from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class PersonalInfo(BaseModel):
    name: str = ""
    headline: Optional[str] = ""   # 👈 cargo profissional
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    start_month: str = ""
    start_year: str = ""
    end_month: Optional[str] = ""
    end_year: Optional[str] = ""
    description: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: str = ""
    degree: str = ""
    field: str = ""
    start_month: str = ""
    start_year: str = ""
    end_month: Optional[str] = ""
    end_year: Optional[str] = ""


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)


class Skills(BaseModel):
    technical: List[str] = Field(default_factory=list)
    soft: List[str] = Field(default_factory=list)


class CV(BaseModel):
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: str = ""
    skills: Skills = Field(default_factory=Skills)
    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    awards: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
