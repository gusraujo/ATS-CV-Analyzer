import json
import re
from app.infra.llm.client import client
from app.prompts.job_extraction import (
    JOB_EXTRACTION_SYSTEM_PROMPT,
    build_job_extraction_prompt
)


def extract_job_to_json(job_text: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {"role": "system", "content": JOB_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": build_job_extraction_prompt(job_text)}
        ]
    )

    raw = response.output_text.strip()
    raw = re.sub(r"^```json|```$", "", raw).strip()

    if not raw.startswith("{"):
        raise ValueError("Invalid JSON returned by LLM")

    return json.loads(raw)