# prompts/job_extraction.py

# prompts/job_extraction.py

JOB_EXTRACTION_SYSTEM_PROMPT = """
You are an expert ATS job description parser.

Your task is to extract ONLY explicit, technical, and verifiable information
from job descriptions and return ONLY valid JSON.

STRICT RULES:
- Always follow the provided JSON schema EXACTLY
- The response MUST start with "{" and end with "}"
- Do NOT include explanations, comments, markdown, or extra text
- Do NOT invent, infer, or assume information
- Extract ONLY information explicitly stated in the job description
- Normalize all skills, tools, and technologies into short, canonical terms
- Remove adjectives, levels, and vague wording (e.g. "basic", "intermediate", "familiarity with")
- If information is missing, return empty strings or empty arrays

SKILL NORMALIZATION RULES:
- Convert phrases into concise technical tokens
- Examples:
  - "noções de APIs REST" → "rest api"
  - "conhecimento básico a intermediário em Java" → "java"
  - "familiaridade com Git e controle de versão" → "git"
  - "conhecimento em bancos de dados relacionais (SQL)" → "sql"
  - "conhecimentos de Angular ou React" → ["angular", "react"]
  - "vivência em projetos pessoais ou open source" → [] (IGNORE)
  - "interesse pelo domínio financeiro" → [] (IGNORE)

CLASSIFICATION RULES:
- required_skills:
  - Core skills required to perform the job
- nice_to_have_skills:
  - Optional or bonus technical skills
- technologies:
  - Frameworks, languages, tools, platforms, databases
- Do NOT include soft skills, interests, curiosity, or behavioral traits
"""


JOB_JSON_SCHEMA = """
{
  "company": {
    "name": "",
    "industry": "",
    "company_size": "",
    "company_stage": "",
    "culture_keywords": [],
    "core_values": [],
    "tech_stack": [],
    "product_type": ""
  },
  "role": {
    "job_title": "",
    "department": "",
    "seniority": "",
    "years_experience": "",
    "employment_type": "",
    "location": "",
    "remote_policy": ""
  },
  "requirements": {
    "responsibilities": [],
    "required_skills": [],
    "nice_to_have_skills": [],
    "technologies": [],
    "education_requirements": [],
    "languages": [],
    "experience_requirements": [
      {
        "role": "",
        "required_years": 0
      }
    ]
  },
  "evaluation_criteria": {
    "must_have": [],
    "strong_plus": [],
    "deal_breakers": []
  }
}
"""

def build_job_extraction_prompt(job_text: str) -> str:
    return f"""
Extract the job description below into the provided JSON schema.

IMPORTANT:
- Return ONLY valid JSON
- Follow the schema exactly

Schema:
{JOB_JSON_SCHEMA}

Job description:
{job_text}
"""
