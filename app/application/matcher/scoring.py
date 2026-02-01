def calculate_overall_score(
    skill_score: float,
    experience_score: float,
    education_score: float,
    weights=None
) -> float:

    weights = weights or {
        "skills": 0.5,
        "experience": 0.35,
        "education": 0.15
    }

    score = (
        skill_score * weights["skills"] +
        experience_score * weights["experience"] +
        education_score * weights["education"]
    )

    return round(score, 2)
