CV_EXTRACTION_SYSTEM_PROMPT = """
You are an expert ATS resume parser.

Your task is to extract structured information from resumes and return ONLY valid JSON.

Rules:
- Always follow the provided JSON schema
- The response MUST start with "{" and end with "}"
- Do NOT include explanations, comments, or markdown
- Do NOT invent information
- If data is missing, return empty strings or empty arrays
- Normalize job titles and technologies when possible
- Extract months and years separately when dates are available
- If only year is available, leave month as empty string
"""

CV_JSON_SCHEMA = """
{
  "personal_info": {
    "name": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "github": ""
  },
  "summary": "",
  "skills": {
    "technical": [],
    "soft": []
  },
  "experience": [
    {
      "company": "",
      "role": "",
      "start_month": "",
      "start_year": "",
      "end_month": "",
      "end_year": "",
      "description": [],
      "technologies": []
    }
  ],
  "education": [
    {
      "institution": "",
      "degree": "",
      "field": "",
      "start_month": "",
      "start_year": "",
      "end_month": "",
      "end_year": ""
    }
  ],
  "certifications": [],
  "awards": [],
  "languages": [],
  "projects": [
    {
      "name": "",
      "description": "",
      "technologies": []
    }
  ]
}
"""

def build_cv_extraction_prompt(resume_text: str) -> str:
    return f"""
Extract the resume below into the following JSON schema.
Return ONLY valid JSON.

Schema:
{CV_JSON_SCHEMA}

Resume:
{resume_text}
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
    "languages": []
  },
  "evaluation_criteria": {
    "must_have": [],
    "strong_plus": [],
    "deal_breakers": []
  }
}
"""


JOB_EXTRACTION_SYSTEM_PROMPT = """
You are an expert ATS job description parser.

Your task is to extract structured information from job descriptions and return ONLY valid JSON.

Rules:
- Always follow the provided JSON schema
- The response MUST start with "{" and end with "}"
- Do NOT include explanations, comments, or markdown
- Do NOT invent information
- If data is missing, return empty strings or empty arrays
- Normalize job titles, skills and technologies
"""

def build_job_extraction_prompt(job_text: str) -> str:
    return f"""
Extract the job description below into the following JSON schema.
Return ONLY valid JSON.

Schema:
{JOB_JSON_SCHEMA}

Job description:
{job_text}
"""
