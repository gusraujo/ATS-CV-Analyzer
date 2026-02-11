from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.application.services.match_service import MatchService
from app.infra.llm.cv_rewriter import rewrite_cv
from app.infra.logging.logger import get_logger

logger = get_logger("process_cv_use_case")


class ProcessCVUseCase:

    def __init__(self):
        self.match_service = MatchService()

    def execute(
        self,
        cv: CV,
        job: Job,
        language: str,
        suggestions: list[str],
        technologies: list[str]
    ) -> tuple[CV, any]:

        logger.info(
            "ProcessCVUseCase started | candidate=%s | role=%s | language=%s | suggestions=%d | technologies=%d",
            cv.personal_info.name,
            job.role.job_title,
            language,
            len(suggestions or []),
            len(technologies or [])
        )

        # =========================
        # MATCH
        # =========================
        logger.info("Running match analysis")
        match_result = self.match_service.execute(cv, job)

        logger.info(
            "Match completed | overall_score=%.2f | recommendation=%s",
            match_result.overall_score,
            match_result.recommendation
        )

        # =========================
        # CV REWRITE (LLM)
        # =========================
        logger.info("Starting CV rewrite via LLM")

        optimized_cv_dict = rewrite_cv(
            cv=cv.model_dump(),
            job=job.model_dump(),
            match_result=match_result.model_dump(),
            language=language,
            suggestions=suggestions,
            technologies=technologies
        )

        logger.info(
            "CV rewrite completed | sections=%d",
            len(optimized_cv_dict.keys())
        )

        # =========================
        # VALIDATION / CONVERSION
        # =========================
        logger.info("Converting rewritten CV JSON to CV model")

        optimized_cv = CV(**optimized_cv_dict)

        logger.info(
            "ProcessCVUseCase finished successfully | candidate=%s",
            optimized_cv.personal_info.name
        )

        return optimized_cv, match_result
