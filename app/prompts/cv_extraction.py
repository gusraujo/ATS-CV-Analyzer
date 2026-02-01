# prompts/cv_extraction.py

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
