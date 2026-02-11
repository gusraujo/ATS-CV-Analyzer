import json
import os
import shutil
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Form, UploadFile, File, Body, HTTPException
from fastapi.responses import FileResponse

from app.domain.models.job import Job
from app.application.usecases.process_cv_use_case import ProcessCVUseCase
from app.infra.llm.cv_extractor import extract_cv_to_json
from app.infra.pdf.reader import read_pdf
from app.infra.pdf.cv_renderer import render_cv_pdf
from app.domain.validators.cv_validator import validate_cv
from app.infra.logging.logger import get_logger

router = APIRouter(prefix="/process", tags=["Process"])
logger = get_logger("process_cv_route")


@router.post("/cv")
async def process_cv(
    file: UploadFile = File(...),
    job: str = Form(...),
    language: str = "en",
    suggestions: list[str] = Body(default=[]),
    technologies: list[str] = Body(default=[])
):
    logger.info("CV processing started")

    if not file.filename.lower().endswith(".pdf"):
        logger.warning("Invalid file type: %s", file.filename)
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        temp_path = temp_pdf.name

    logger.info("Temporary PDF saved at %s", temp_path)

    try:
        # Job parsing
        job_dict = json.loads(job)
        job_obj = Job(**job_dict)
        logger.info("Job parsed successfully: %s", job_obj.role.job_title)

        # PDF reading
        resume_text = read_pdf(temp_path)
        logger.info("PDF read successfully (%d chars)", len(resume_text))

        # CV extraction
        cv_raw = extract_cv_to_json(resume_text)
        logger.info("CV extracted from LLM")

        # Validation
        cv = validate_cv(cv_raw)
        logger.info("CV validated successfully")

        # Use case
        use_case = ProcessCVUseCase()
        optimized_cv, match_result = use_case.execute(
            cv=cv,
            job=job_obj,
            language=language,
            suggestions=suggestions,
            technologies=technologies
        )
        logger.info(
            "CV processed successfully | Overall score: %.2f",
            match_result.overall_score
        )

        # PDF rendering
        candidate_name = optimized_cv.personal_info.name.replace(" ", "_")
        output_path = f"output/CV_{candidate_name}_{language}.pdf"

        render_cv_pdf(
            cv=optimized_cv,
            output_path=output_path,
            language=language
        )

        logger.info("Optimized CV PDF generated at %s", output_path)

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        logger.exception("Unexpected error during CV processing")
        raise

    finally:
        os.remove(temp_path)
        logger.info("Temporary file removed")
