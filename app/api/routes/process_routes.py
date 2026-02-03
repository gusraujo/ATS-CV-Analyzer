import json
from fastapi import APIRouter, Form, UploadFile, File, Body, HTTPException
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
import shutil
import os

from app.domain.models.job import Job
from app.application.usecases.process_cv_use_case import ProcessCVUseCase
from app.infra.llm.cv_extractor import extract_cv_to_json
from app.infra.pdf.reader import read_pdf
from app.infra.pdf.cv_renderer import render_cv_pdf
from app.domain.validators.cv_validator import validate_cv

router = APIRouter(prefix="/process", tags=["Process"])


@router.post("/cv")
async def process_cv(
    file: UploadFile = File(...),
    job: str = Form(...),
    language: str = "en",
    suggestions: list[str] = Body(default=[])
):
    """
    Recebe:
    - CV em PDF
    - Job já estruturado
    Retorna:
    - CV otimizado em PDF
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        temp_path = temp_pdf.name

    try:
        job_dict = json.loads(job)
        job_obj = Job(**job_dict)
        
        resume_text = read_pdf(temp_path)
        cv_raw = extract_cv_to_json(resume_text)
        cv = validate_cv(cv_raw)

        use_case = ProcessCVUseCase()
        optimized_cv, match_result = use_case.execute(
            cv=cv,
            job=job_obj,
            language=language,
            suggestions=suggestions
        )

        candidate_name = optimized_cv.personal_info.name.replace(" ", "_")
        output_path = f"output/CV_{candidate_name}_{language}.pdf"

        render_cv_pdf(
            cv=optimized_cv,
            output_path=output_path,
            language=language
        )

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=os.path.basename(output_path)
        )
    finally:
        os.remove(temp_path)