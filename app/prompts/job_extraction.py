# prompts/job_extraction.py

JOB_EXTRACTION_SYSTEM_PROMPT = """
You are an expert ATS job description parser.

Your task is to extract structured information from job descriptions and return ONLY valid JSON.

STRICT RULES:
- Always follow the provided JSON schema EXACTLY
- The response MUST start with "{" and end with "}"
- Do NOT include explanations, comments, markdown, or extra text
- Do NOT invent or infer information
- Normalize job titles, skills, and technologies
- If information is missing, return empty strings or empty arrays
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
