from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import EducationMatchDetails


EDUCATION_RANK = {
    "high school": 1,
    "associate": 2,
    "bachelor": 3,
    "master": 4,
    "phd": 5
}


def match_education(cv: CV, job: Job) -> EducationMatchDetails:
    # Se o job não especificou requisitos de educação
    if not job.requirements.education_requirements:
        return EducationMatchDetails(
            score=100,
            degree=[edu.degree for edu in cv.education],
            justification="No education requirement specified."
        )

    # Pega os graus do CV (lista de strings)
    cv_degrees = [edu.degree.lower() for edu in cv.education]

    # Pega os requisitos do Job (lista de strings)
    job_degrees = [req.lower() for req in job.requirements.education_requirements]

    # Contabiliza quantos requisitos foram atendidos
    matched = [deg for deg in cv_degrees if deg in job_degrees]
    score = round(len(matched) / len(job_degrees) * 100, 2) if job_degrees else 100

    justification = (
        f"Candidate degrees: {cv_degrees}. "
        f"Required: {job_degrees}. "
        f"Matched: {matched}."
    )

    return EducationMatchDetails(
        score=score,
        degree=[edu.degree for edu in cv.education],
        justification=justification
    )

