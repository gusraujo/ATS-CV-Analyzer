from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.domain.models.match import MatchResult, MatchDetails
from app.application.matcher.skill_matcher import match_skills
from app.application.matcher.experience_matcher import match_experience
from app.application.matcher.education_matcher import match_education
from app.application.matcher.scoring import calculate_overall_score
from app.infra.logging.logger import get_logger

logger = get_logger("match_service")


class MatchService:

    def execute(self, cv: CV, job: Job) -> MatchResult:
        logger.info(
            "MatchService started | candidate=%s | role=%s",
            cv.personal_info.name,
            job.role.job_title
        )

        # Skills
        skill_result = match_skills(cv, job)
        logger.info(
            "Skill match completed | score=%.2f | matched=%d | missing=%d",
            skill_result["score"],
            len(skill_result["matched"]),
            len(skill_result["missing"])
        )

        # Experience
        experience_result = match_experience(cv, job)
        logger.info(
            "Experience match completed | score=%.2f",
            experience_result.score
        )

        # Education
        education_result = match_education(cv, job)
        logger.info(
            "Education match completed | score=%.2f",
            education_result.score
        )

        # Overall
        overall = calculate_overall_score(
            skill_result["score"],
            experience_result.score,
            education_result.score
        )

        recommendation = self._recommendation(overall)

        logger.info(
            "Overall match calculated | score=%.2f | recommendation=%s",
            overall,
            recommendation
        )

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

    def _strengths(self, s: dict, e, edu):
        result = []
        if s["score"] >= 80:
            result.append("Strong skill match")
        if e.score >= 70:
            result.append("Relevant professional experience")
        if edu.score == 100:
            result.append("Education level meets or exceeds requirement")
        return result

    def _gaps(self, s: dict, e, edu):
        result = []
        if s["missing"]:
            result.append("Missing required skills")
        if e.score < 60:
            result.append("Insufficient experience")
        if edu.score < 100:
            result.append("Education level below requirement")
        return result
