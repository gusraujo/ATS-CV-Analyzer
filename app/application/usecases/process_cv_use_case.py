from app.domain.models.cv import CV
from app.domain.models.job import Job
from app.application.services.match_service import MatchService
from app.infra.llm.cv_rewriter import rewrite_cv


class ProcessCVUseCase:

    def __init__(self):
        self.match_service = MatchService()

    def execute(self, cv: CV, job: Job, language: str):
        match_result = self.match_service.execute(cv, job)

        optimized_cv_dict = rewrite_cv(
            cv=cv.model_dump(),
            job=job.model_dump(),
            match_result=match_result.model_dump(),
            language=language
        )

        optimized_cv = CV(**optimized_cv_dict)

        return optimized_cv, match_result
