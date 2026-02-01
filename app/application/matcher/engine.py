from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import MatchDetails
from app.application.matcher.skill_matcher import match_skills
from app.application.matcher.experience_matcher import match_experience
from app.application.matcher.education_matcher import match_education


def run_match_engine(cv: CV, job: Job) -> MatchDetails:
    return MatchDetails(
        skills=match_skills(cv, job),
        experience=match_experience(cv, job),
        education=match_education(cv, job)
    )