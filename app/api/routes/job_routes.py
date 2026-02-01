from fastapi import APIRouter, HTTPException
import logging

from app.api.dto.job_input_dto import JobDescriptionInput
from app.domain.models.job import Job
from app.application.services.extract_job_service import extract_job_to_json

router = APIRouter(prefix="/jobs", tags=["Jobs"])

logger = logging.getLogger(__name__)


@router.post("/extract", response_model=Job)
async def extract_job_from_description(payload: JobDescriptionInput):
    """
    Recebe um texto grande de job description
    e retorna o Job estruturado (JSON).
    """
    logger.info("Starting job extraction")
    logger.debug(f"Job description size: {len(payload.job_description)} chars")

    try:
        job_json = extract_job_to_json(payload.job_description)

        logger.info("Job extraction completed successfully")
        logger.debug(f"Extracted job: {job_json}")

        return Job(**job_json)

    except Exception as e:
        logger.exception("Error while extracting job description")
        raise HTTPException(status_code=400, detail=str(e))
