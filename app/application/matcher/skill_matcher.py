# app/application/matcher/skill_matcher.py
from typing import List

def match_skills(
    cv_skills: List[str],
    job_required: List[str]
) -> dict:
    matched = list(set(cv_skills) & set(job_required))
    missing = list(set(job_required) - set(cv_skills))

    score = 0
    if job_required:
        score = len(matched) / len(job_required) * 100

    return {
        "score": round(score, 2),
        "matched": matched,
        "missing": missing,
        "justification": (
            f"{len(matched)} of {len(job_required)} required skills matched."
        )
    }