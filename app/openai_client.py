# openai_client.py
import re
from openai import OpenAI
import os
import json
from prompts import (
    CV_EXTRACTION_SYSTEM_PROMPT,
    build_cv_extraction_prompt
)
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_cv_to_json(resume_text: str) -> dict:
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {
                "role": "system",
                "content": CV_EXTRACTION_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": build_cv_extraction_prompt(resume_text)
            }
        ]
    )

    raw_output = response.output_text.strip()

    # 🛡️ Remove markdown fences if model ignored instructions
    raw_output = re.sub(r"^```json|```$", "", raw_output).strip()

    if not raw_output.startswith("{"):
        raise ValueError(f"Model output is not JSON:\n{raw_output[:500]}")

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by model.\n"
            f"Error: {e}\n"
            f"Output:\n{raw_output[:500]}"
        )