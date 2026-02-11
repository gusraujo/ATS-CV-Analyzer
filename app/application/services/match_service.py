import logging

from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import MatchResult, MatchDetails
from app.application.matcher.skill_matcher import match_skills
from app.application.matcher.experience_matcher import match_experience
from app.application.matcher.education_matcher import match_education
from app.application.matcher.scoring import calculate_overall_score

logger = logging.getLogger(__name__)


class MatchService:

    def execute(self, cv: CV, job: Job) -> MatchResult:
        logger.info("Starting match process")
        logger.debug("CV id/name: %s", getattr(cv.personal_info, "name", "N/A"))
        logger.debug("Job title: %s", getattr(job, "title", "N/A"))

        # Extrair skills do CV
        cv_skills = cv.skills.technical + cv.skills.soft
        logger.info("Extracted %d CV skills", len(cv_skills))

        # Extrair skills do Job
        job_skills = job.requirements.required_skills + job.requirements.nice_to_have_skills
        logger.info("Extracted %d Job skills", len(job_skills))

        # Rodar os matchers
        logger.info("Running skill matcher")
        skill_result = match_skills(cv_skills, job_skills)

        logger.info(
            "Skill match score=%s | matched=%d | missing=%d",
            skill_result["score"],
            len(skill_result["matched"]),
            len(skill_result["missing"]),
        )

        logger.info("Running experience matcher")
        experience_result = match_experience(cv, job)
        logger.info("Experience score=%s", experience_result.score)

        logger.info("Running education matcher")
        education_result = match_education(cv, job)
        logger.info("Education score=%s", education_result.score)

        overall = calculate_overall_score(
            skill_result["score"],
            experience_result.score,
            education_result.score
        )

        logger.info("Overall match score calculated: %s", overall)

        recommendation = self._recommendation(overall)
        logger.info("Final recommendation: %s", recommendation)

        result = MatchResult(
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

        logger.info("Match process finished successfully")
        return result

    def _recommendation(self, score: float) -> str:
        if score >= 80:
            return "STRONG"
        if score >= 60:
            return "PARTIAL"
        return "WEAK"

    def _strengths(self, s, e, edu):
        result = []
        if s["score"] >= 80:
            result.append("Strong skill match")
        if e.score >= 70:
            result.append("Relevant professional experience")
        if edu.score == 100:
            result.append("Education level meets or exceeds requirement")

        logger.debug("Strengths identified: %s", result)
        return result

    def _gaps(self, s, e, edu):
        result = []
        if s["missing"]:
            result.append("Missing required skills")
        if e.score < 60:
            result.append("Insufficient experience")
        if edu.score < 100:
            result.append("Education level below requirement")

        logger.debug("Gaps identified: %s", result)
        return result
