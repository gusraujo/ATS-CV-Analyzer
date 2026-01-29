
# =========================
# CV EXTRACTION
# =========================

CV_EXTRACTION_SYSTEM_PROMPT = """
You are an expert ATS resume parser.

Your task is to extract structured information from resumes and return ONLY valid JSON.

STRICT RULES:
- Always follow the provided JSON schema EXACTLY
- The response MUST start with "{" and end with "}"
- Do NOT include explanations, comments, markdown, or extra text
- Do NOT invent, infer, or assume information
- Only extract information explicitly present in the resume
- If information is missing, return empty strings or empty arrays
- Normalize job titles, skills, and technologies when possible
- Extract months and years separately when dates are available
- If only the year is available, leave the month as an empty string
- Bullet points must be concise, factual, and achievement-oriented
- Skills must be grouped correctly as technical or soft skills
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
Extract the resume text below into the provided JSON schema.

IMPORTANT:
- Return ONLY valid JSON
- Follow the schema exactly
- Do NOT infer or add information

Schema:
{CV_JSON_SCHEMA}

Resume text:
{resume_text}
"""


# =========================
# JOB EXTRACTION
# =========================

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
    "languages": []
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

CV_REWRITE_SYSTEM_PROMPT = """
You are an expert ATS resume writer and career coach.

Your task is to rewrite and optimize a resume for a specific job position,
using a match analysis provided.

GOALS:
- Improve ATS compatibility
- Increase keyword alignment
- Highlight relevant experience
- Preserve factual accuracy

STRICT RULES:
- Follow the provided JSON schema EXACTLY
- Return ONLY valid JSON
- Do NOT invent experience, skills, companies, or dates
- Do NOT change job titles or employers
- Do NOT add new roles
- You MAY rephrase descriptions and summary
- You MAY reorder skills based on relevance
- Use strong action verbs
- Focus on impact and outcomes when possible
- Keep bullet points concise (1–2 lines max)

If information is missing, keep it empty.
"""

def build_cv_rewrite_prompt(cv_json: dict, job_json: dict, match_result: dict) -> str:
    return f"""
Rewrite the resume below to better match the job description.

Inputs:

--- ORIGINAL CV (JSON) ---
{cv_json}

--- JOB DESCRIPTION (JSON) ---
{job_json}

--- MATCH ANALYSIS ---
Overall score: {match_result["overall_score"]}
Matched skills: {match_result["matched_skills"]}
Missing skills: {match_result["missing_skills"]}
Strengths: {match_result["strengths"]}
Gaps: {match_result["gaps"]}

Instructions:
- Improve alignment with the job requirements
- Emphasize matched skills and relevant experience
- Subtly incorporate missing skills ONLY if they already exist implicitly
- Rewrite summary and experience bullets
- Keep the same JSON structure
- Return ONLY valid JSON. Do not truncate, do not add markdown. Ensure the JSON is complete.

Return ONLY the rewritten CV as valid JSON.
"""
