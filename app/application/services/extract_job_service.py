import json
import logging
import re

from app.infra.llm.client import client
from app.prompts.job_extraction import (
    JOB_EXTRACTION_SYSTEM_PROMPT,
    build_job_extraction_prompt,
)

logger = logging.getLogger(__name__)


def extract_job_to_json(job_description: str) -> dict:
    """
    Envia o texto da Job Description para o modelo LLM
    e retorna um JSON estruturado conforme o JobSchema.
    """

    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty")

    logger.info("Sending job description to LLM")
    logger.debug(f"Job description length: {len(job_description)}")

    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {
                "role": "system",
                "content": JOB_EXTRACTION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_job_extraction_prompt(job_description),
            },
        ],
    )

    raw_output = response.output_text.strip()

    logger.debug(f"Raw LLM output (first 500 chars): {raw_output[:500]}")

    # 🛡️ Remove possíveis fences de markdown
    raw_output = re.sub(r"^```json|```$", "", raw_output).strip()

    if not raw_output.startswith("{"):
        logger.error("LLM output is not JSON")
        raise ValueError(f"Model output is not JSON:\n{raw_output[:500]}")

    try:
        job_json = json.loads(raw_output)
        logger.info("Job extraction JSON parsed successfully")
        return job_json

    except json.JSONDecodeError as e:
        logger.exception("Invalid JSON returned by LLM")
        raise ValueError(
            f"Invalid JSON returned by model.\nError: {e}\nOutput:\n{raw_output[:500]}"
        )
