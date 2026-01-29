from pydantic import BaseModel
from typing import List, Optional, Dict


class SkillMatchDetails(BaseModel):
    score: float
    matched: List[str]
    missing: List[str]
    justification: str


class ExperienceMatchDetails(BaseModel):
    score: float
    matched_roles: List[str]
    years_considered: Optional[int] = 0
    justification: str


class EducationMatchDetails(BaseModel):
    score: float
    degree: Optional[str]
    justification: str


class MatchDetails(BaseModel):
    skills: SkillMatchDetails
    experience: ExperienceMatchDetails
    education: EducationMatchDetails


class MatchResult(BaseModel):
    # Scores principais
    overall_score: float  # 0 - 100
    skill_score: float
    experience_score: float
    education_score: float

    # Resultado de skills
    matched_skills: List[str]
    missing_skills: List[str]

    # Análise qualitativa
    strengths: List[str]
    gaps: List[str]

    # Classificação final
    recommendation: str  # Strong / Partial / Weak

    # 🔥 Explicabilidade ATS
    details: MatchDetails
