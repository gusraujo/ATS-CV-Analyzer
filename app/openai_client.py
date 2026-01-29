# openai_client.py
import re
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import (
    CV_EXTRACTION_SYSTEM_PROMPT,
    CV_REWRITE_SYSTEM_PROMPT,
    build_cv_extraction_prompt,
    build_cv_rewrite_prompt
)

# Carrega variáveis de ambiente
load_dotenv()

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_cv_to_json(resume_text: str) -> dict:
    """
    Envia o texto do CV para o modelo GPT e retorna JSON estruturado conforme o schema.
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        temperature=0,
        input=[
            {"role": "system", "content": CV_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": build_cv_extraction_prompt(resume_text)}
        ]
    )

    raw_output = response.output_text.strip()

    # 🛡️ Remove possíveis fences de markdown
    raw_output = re.sub(r"^```json|```$", "", raw_output).strip()

    if not raw_output.startswith("{"):
        raise ValueError(f"Model output is not JSON:\n{raw_output[:500]}")

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by model.\nError: {e}\nOutput:\n{raw_output[:500]}"
        )


def rewrite_cv(
    cv: dict,
    job: dict,
    match_result: dict,
    language: str,
    suggestions: list[str] = None
) -> dict:
    """
    Reescreve o CV com base na análise do match, usando o modelo GPT.
    language: 'pt' = Português, 'en' = Inglês
    """

    prompt = build_cv_rewrite_prompt(cv, job, match_result, language=language, suggestions=suggestions)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": CV_REWRITE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON returned by rewrite_cv.\nError: {e}\nOutput:\n{content[:500]}"
        )
