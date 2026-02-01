from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import ExperienceMatchDetails


def match_experience(cv: CV, job: Job) -> ExperienceMatchDetails:
    matched_roles = []
    total_years = 0
    required_years = 0

    for req in job.requirements.experience_requirements:
        required_years += req.required_years or 0
        for exp in cv.experience:
            if req.role.lower() in exp.role.lower():
                matched_roles.append(exp.role)
                total_years += exp.years

    if required_years == 0:
        score = 100
    else:
        score = min((total_years / required_years) * 100, 100)

    justification = (
        f"Matched roles: {matched_roles}. "
        f"Considered {total_years} years out of {required_years} required."
    )

    return ExperienceMatchDetails(
        score=round(score, 2),
        matched_roles=list(set(matched_roles)),
        years_considered=total_years,
        justification=justification
    )