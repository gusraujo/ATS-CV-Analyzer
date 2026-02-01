from pydantic import BaseModel
from typing import List


class SkillMatchDetails(BaseModel):
    score: float  # 0 - 100
    matched: List[str] = []
    missing: List[str] = []
    justification: str = ""


class ExperienceMatchDetails(BaseModel):
    score: float  # 0 - 100
    matched_roles: List[str] = []
    years_considered: int = 0
    justification: str = ""


class EducationMatchDetails(BaseModel):
    score: float
    degree: list[str] = []
    justification: str


class MatchDetails(BaseModel):
    skills: SkillMatchDetails
    experience: ExperienceMatchDetails
    education: EducationMatchDetails


class MatchResult(BaseModel):
    # =========================
    # SCORES
    # =========================
    overall_score: float  # 0 - 100
    skill_score: float
    experience_score: float
    education_score: float

    # =========================
    # SKILLS
    # =========================
    matched_skills: List[str] = []
    missing_skills: List[str] = []

    # =========================
    # QUALITATIVE ANALYSIS
    # =========================
    strengths: List[str] = []
    gaps: List[str] = []

    # =========================
    # FINAL CLASSIFICATION
    # =========================
    recommendation: str  # Strong / Partial / Weak

    # =========================
    # ATS EXPLAINABILITY
    # =========================
    details: MatchDetails
