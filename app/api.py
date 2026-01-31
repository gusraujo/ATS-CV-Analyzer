from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
import shutil
import os
import logging

from app.models.cv import CV
from app.schemas.job_schema import JobSchema
from app.services.cv_renderer import render_cv_pdf
from app.services.match_service import run_match
from app.pdf_reader import read_pdf
from app.openai_client import (
    extract_cv_to_json,
    extract_job_to_json,
    rewrite_cv
)
from app.validators.cv_validator import validate_cv

# =========================
# LOG CONFIG
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ATS CV API")


@app.post("/process_cv/")
async def process_cv(
    file: UploadFile = File(...),
    job_description: str = Body(..., embed=True),
    language: str = "pt"
):
    logger.info("🚀 New CV processing request received")
    logger.info(f"📄 File received: {file.filename}")
    logger.info(f"🌍 Language selected: {language}")

    if not file.filename.lower().endswith(".pdf"):
        logger.error("❌ Invalid file type (not PDF)")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # =========================
    # 1️⃣ Save CV PDF
    # =========================
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        shutil.copyfileobj(file.file, temp_pdf)
        temp_pdf_path = temp_pdf.name

    logger.info(f"📁 Temporary PDF saved at {temp_pdf_path}")

    try:
        # =========================
        # 2️⃣ Read CV
        # =========================
        logger.info("📖 Reading CV PDF...")
        resume_text = read_pdf(temp_pdf_path)
        logger.info(f"📝 CV text extracted ({len(resume_text)} chars)")

        # =========================
        # 3️⃣ Extract CV
        # =========================
        logger.info("🤖 Extracting CV JSON with LLM...")
        cv_raw = extract_cv_to_json(resume_text)
        cv: CV = validate_cv(cv_raw)
        logger.info(f"✅ CV validated for candidate: {cv.personal_info.name}")

        # =========================
        # 4️⃣ Extract JOB
        # =========================
        logger.info("📋 Extracting job description JSON...")
        job_json = extract_job_to_json(job_description)
        job = JobSchema(**job_json)
        logger.info(f"🏢 Job extracted: {job.title}")

        # =========================
        # 5️⃣ Match
        # =========================
        logger.info("🧠 Running ATS match engine...")
        match_result = run_match(cv, job)
        logger.info(f"📊 Match score: {match_result.overall_score}")

        # =========================
        # 6️⃣ Rewrite CV
        # =========================
        logger.info("✍️ Rewriting CV based on match and language...")
        optimized_cv_json = rewrite_cv(
            cv=cv.model_dump(),
            job=job.model_dump(),
            match_result=match_result.model_dump(),
            language=language
        )

        optimized_cv = CV(**optimized_cv_json)
        logger.info("✅ CV rewrite completed")

        # =========================
        # 7️⃣ Render PDF
        # =========================
        candidate_name = optimized_cv.personal_info.name.replace(" ", "_")
        output_path = f"output/CV_{candidate_name}_{language}.pdf"

        logger.info(f"📄 Rendering PDF: {output_path}")
        render_cv_pdf(
            cv=optimized_cv,
            output_path=output_path,
            language=language
        )

        logger.info("🎉 CV PDF successfully generated")

        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename=os.path.basename(output_path)
        )

    except Exception as e:
        logger.exception("🔥 Error during CV processing")
        raise e

    finally:
        logger.info("🧹 Cleaning up temporary files")
        os.remove(temp_pdf_path)
