from pydantic import BaseModel
from typing import List


# =========================
# COMPANY
# =========================

class Company(BaseModel):
    name: str = ""
    industry: str = ""
    company_size: str = ""
    company_stage: str = ""
    culture_keywords: List[str] = []
    core_values: List[str] = []
    tech_stack: List[str] = []
    product_type: str = ""


# =========================
# ROLE
# =========================

class Role(BaseModel):
    job_title: str = ""
    department: str = ""
    seniority: str = ""
    years_experience: str = ""
    employment_type: str = ""
    location: str = ""
    remote_policy: str = ""


# =========================
# REQUIREMENTS
# =========================

class ExperienceRequirement(BaseModel):
    role: str
    required_years: int = 0

class Requirements(BaseModel):
    responsibilities: List[str] = []
    required_skills: List[str] = []
    nice_to_have_skills: List[str] = []
    technologies: List[str] = []
    education_requirements: List[str] = []
    languages: List[str] = []
    experience_requirements: List[ExperienceRequirement] = []


# =========================
# EVALUATION
# =========================

class EvaluationCriteria(BaseModel):
    must_have: List[str] = []
    strong_plus: List[str] = []
    deal_breakers: List[str] = []


# =========================
# JOB SCHEMA
# =========================

class Job(BaseModel):
    company: Company
    role: Role
    requirements: Requirements
    evaluation_criteria: EvaluationCriteria
