import logging
from typing import List

logger = logging.getLogger(__name__)


def match_skills(
    cv_skills: List[str],
    job_required: List[str]
) -> dict:
    missing_data = []

    if not cv_skills:
        missing_data.append("CV has no skills listed")

    if not job_required:
        missing_data.append("Job has no required skills defined")

    logger.info(
        "Starting skill matching | cv_skills=%d | job_skills=%d",
        len(cv_skills),
        len(job_required)
    )

    if not job_required:
        return {
            "score": 0.0,
            "matched": [],
            "missing": [],
            "missing_data": missing_data,
            "justification": "Job does not define required skills."
        }

    cv_set = set(map(str.lower, cv_skills))
    job_set = set(map(str.lower, job_required))

    matched = list(cv_set & job_set)
    missing = list(job_set - cv_set)

    score = len(matched) / len(job_required) * 100

    logger.info(
        "Skill match | score=%.2f | matched=%d | missing=%d",
        score,
        len(matched),
        len(missing)
    )

    if missing:
        logger.warning("Missing required skills: %s", missing)

    if missing_data:
        logger.warning("Missing input data: %s", missing_data)

    return {
        "score": round(score, 2),
        "matched": matched,
        "missing": missing,
        "missing_data": missing_data,
        "justification": (
            f"{len(matched)} of {len(job_required)} required skills matched."
        )
    }
