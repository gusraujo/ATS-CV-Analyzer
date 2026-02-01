import json
import re
from app.infra.llm.client import client
from app.prompts.cv_extraction import (
    CV_EXTRACTION_SYSTEM_PROMPT,
    build_cv_extraction_prompt
)


def extract_cv_to_json(resume_text: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {"role": "system", "content": CV_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": build_cv_extraction_prompt(resume_text)}
        ]
    )

    raw = response.output_text.strip()
    raw = re.sub(r"^```json|```$", "", raw).strip()

    if not raw.startswith("{"):
        raise ValueError("Invalid JSON returned by LLM")

    return json.loads(raw)
