from pydantic import BaseModel
from typing import List


class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""


class Skills(BaseModel):
    technical: List[str] = []
    soft: List[str] = []


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    start_month: str = ""
    start_year: str = ""
    end_month: str = ""
    end_year: str = ""
    description: List[str] = []
    technologies: List[str] = []


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
    technologies: List[str] = []


class CV(BaseModel):
    personal_info: PersonalInfo
    summary: str = ""
    skills: Skills
    experience: List[Experience] = []
    education: List[Education] = []
    certifications: List[str] = []
    awards: List[str] = []
    languages: List[str] = []
    projects: List[Project] = []
