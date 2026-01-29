from pydantic import BaseModel, Field
from typing import List


class Company(BaseModel):
    name: str = ""
    industry: str = ""
    company_size: str = ""
    company_stage: str = ""
    culture_keywords: List[str] = Field(default_factory=list)
    core_values: List[str] = Field(default_factory=list)
    tech_stack: List[str] = Field(default_factory=list)
    product_type: str = ""


class Role(BaseModel):
    job_title: str = ""
    department: str = ""
    seniority: str = ""
    years_experience: str = ""
    employment_type: str = ""
    location: str = ""
    remote_policy: str = ""


class Requirements(BaseModel):
    responsibilities: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    nice_to_have_skills: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    education_requirements: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)


class EvaluationCriteria(BaseModel):
    must_have: List[str] = Field(default_factory=list)
    strong_plus: List[str] = Field(default_factory=list)
    deal_breakers: List[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    company: Company = Company()
    role: Role = Role()
    requirements: Requirements = Requirements()
    evaluation_criteria: EvaluationCriteria = EvaluationCriteria()
