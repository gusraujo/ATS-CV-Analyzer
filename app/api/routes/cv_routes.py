from fastapi import APIRouter, UploadFile, File, HTTPException
from tempfile import NamedTemporaryFile
import shutil
import os

from app.domain.models.cv import CV
from app.infra.llm.cv_extractor import extract_cv_to_json
from app.infra.pdf.reader import read_pdf
from app.domain.validators.cv_validator import validate_cv

router = APIRouter(prefix="/cvs", tags=["CVs"])


@router.post("/extract", response_model=CV)
async def extract_cv(file: UploadFile = File(...)):
    """
    Recebe um CV em PDF e retorna o CV estruturado.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        temp_path = temp_pdf.name

    try:
        resume_text = read_pdf(temp_path)
        cv_raw = extract_cv_to_json(resume_text)
        cv = validate_cv(cv_raw)
        return cv
    finally:
        os.remove(temp_path)
