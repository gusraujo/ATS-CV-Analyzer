import json
import re
from app.infra.llm.client import client
from app.prompts.cv_rewrite import (
    CV_REWRITE_SYSTEM_PROMPT,
    build_cv_rewrite_prompt
)


def rewrite_cv(
    cv: dict,
    job: dict,
    match_result: dict,
    language: str
) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        input=[
            {"role": "system", "content": CV_REWRITE_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_cv_rewrite_prompt(
                    cv_json=cv,
                    job_json=job,
                    match_result=match_result,
                    language=language
                )
            }
        ]
    )

    raw = response.output_text.strip()
    raw = re.sub(r"^```json|```$", "", raw).strip()

    return json.loads(raw)
