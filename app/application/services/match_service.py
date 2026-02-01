from app.domain.models import cv
from app.domain.models import job
from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import MatchResult, MatchDetails
from app.application.matcher.skill_matcher import match_skills
from app.application.matcher.experience_matcher import match_experience
from app.application.matcher.education_matcher import match_education
from app.application.matcher.scoring import calculate_overall_score


class MatchService:

    def execute(self, cv: CV, job: Job) -> MatchResult:
        # Extrair skills do CV
        cv_skills = cv.skills.technical + cv.skills.soft

        # Extrair skills do Job
        job_skills = job.requirements.required_skills + job.requirements.nice_to_have_skills

        # Rodar os matchers
        skill_result = match_skills(cv_skills, job_skills)  # dict
        experience_result = match_experience(cv, job)       # objeto com .score
        education_result = match_education(cv, job)        # objeto com .score

        overall = calculate_overall_score(
            skill_result["score"],          # ⚡ pega o score do dict
            experience_result.score,
            education_result.score
        )

        recommendation = self._recommendation(overall)

        return MatchResult(
            overall_score=overall,
            skill_score=skill_result["score"],
            experience_score=experience_result.score,
            education_score=education_result.score,
            matched_skills=skill_result["matched"],
            missing_skills=skill_result["missing"],
            strengths=self._strengths(skill_result, experience_result, education_result),
            gaps=self._gaps(skill_result, experience_result, education_result),
            recommendation=recommendation,
            details=MatchDetails(
                skills=skill_result,
                experience=experience_result,
                education=education_result
            )
        )

    def _recommendation(self, score: float) -> str:
        if score >= 80:
            return "STRONG"
        if score >= 60:
            return "PARTIAL"
        return "WEAK"

    def _strengths(self, s, e, edu):
        result = []
        if s["score"] >= 80:         # ⚡ usar s["score"]
            result.append("Strong skill match")
        if e.score >= 70:
            result.append("Relevant professional experience")
        if edu.score == 100:
            result.append("Education level meets or exceeds requirement")
        return result

    def _gaps(self, s, e, edu):
        result = []
        if s["missing"]:             # ⚡ usar s["missing"]
            result.append("Missing required skills")
        if e.score < 60:
            result.append("Insufficient experience")
        if edu.score < 100:
            result.append("Education level below requirement")
        return result
