# prompts/cv_rewrite.py

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

def build_cv_rewrite_prompt(
    cv_json: dict,
    job_json: dict,
    match_result: dict,
    language: str = "pt",
    suggestions: list[str] | None = None,
) -> str:
    lang_instruction = (
        "Gere o currículo em português."
        if language == "pt"
        else "Generate the resume in English."
    )

    suggestions_text = ""
    if suggestions:
        suggestions_text = (
            "Additional suggestions to maximize ATS score:\n"
            + "\n".join(f"- {s}" for s in suggestions)
        )

    return f"""
Rewrite the resume below to better match the job description.

{lang_instruction}

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
- Return ONLY valid JSON. Ensure the JSON is complete.

{suggestions_text}
"""
