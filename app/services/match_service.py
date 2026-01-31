from app.services.match_engine import (
    match_skills,
    match_experience,
    match_education
)
from app.services.skill_aliases import load_skill_aliases
from app.schemas.match_result import MatchResult


def run_match(cv, job) -> MatchResult:
    # =========================
    # SKILLS
    # =========================
    cv_technical_skills = cv.skills.technical

    skill_aliases = load_skill_aliases("skill_aliases.txt")

    skills_result = match_skills(
        cv_skills=cv_technical_skills,
        job_skills=job.required_skills,
        skill_aliases=skill_aliases
    )


    # =========================
    # EXPERIENCE
    # =========================
    experience_result = match_experience(
        cv.experience,
        job.experience_requirements
    )

    # =========================
    # EDUCATION
    # =========================
    education_result = match_education(
        cv.education,
        job.education_level
    )

    # =========================
    # WEIGHTED SCORE
    # =========================
    overall = (
        skills_result["score"] * 0.4 +
        experience_result["score"] * 0.35 +
        education_result["score"] * 0.15
    )

    overall = round(overall, 2)

    # =========================
    # RECOMMENDATION
    # =========================
    if overall >= 80:
        recommendation = "Strong Match"
    elif overall >= 60:
        recommendation = "Partial Match"
    else:
        recommendation = "Weak Match"

    # =========================
    # BUILD RESULT
    # =========================
    result = {
        "overall_score": overall,
        "recommendation": recommendation,

        # Scores achatados
        "skill_score": skills_result["score"],
        "experience_score": experience_result["score"],
        "education_score": education_result["score"],

        # Skills
        "matched_skills": skills_result["matched"],
        "missing_skills": skills_result["missing"],

        # Análise qualitativa
        "strengths": skills_result["matched"][:3],
        "gaps": skills_result["missing"][:3],

        # Detalhes explicáveis (ATS-friendly)
        "details": {
            "skills": skills_result,
            "experience": experience_result,
            "education": education_result,
        }
    }

    # =========================
    # Pydantic validation
    # =========================
    return MatchResult(**result)
