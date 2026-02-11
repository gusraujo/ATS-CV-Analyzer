# prompts/cv_rewrite.py

import json


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
    language: str = "en",
    suggestions: list[str] | None = None,
    technologies: list[str] | None = None
) -> str:

    import json

    lang_instruction = (
        "IMPORTANT: The entire output MUST be written in Brazilian Portuguese. "
        "Do NOT use English anywhere in the JSON."
        if language == "pt"
        else
        "IMPORTANT: The entire output MUST be written in English. "
        "Do NOT use Portuguese anywhere in the JSON."
    )

    cv_text = json.dumps(cv_json, ensure_ascii=False, indent=2)
    job_text = json.dumps(job_json, ensure_ascii=False, indent=2)

    suggestions_text = ""
    if suggestions:
        suggestions_text = (
            "\nAdditional suggestions to maximize ATS score:\n"
            + "\n".join(f"- {s}" for s in suggestions)
        )

    technologies_text = ""
    if technologies:
        technologies_text = (
            "\nMANDATORY TECHNOLOGIES TO ADD TO skills.technical:\n"
            + "\n".join(f"- {t}" for t in technologies)
        )

    return f"""
You are an expert ATS resume writer and career coach.

Rewrite the resume below to better match the job description.

{lang_instruction}

LANGUAGE NORMALIZATION RULES:
- When the target language is English:
  - Translate job titles, education titles, section names, locations, and month names to English
  - Keep company names, institution names, and certifications EXACTLY as written
- When the target language is Portuguese:
  - Translate job titles, education titles, section names, locations, and month names to Portuguese
- Dates must keep the same timeline, only month names may be translated

--- ORIGINAL CV (JSON) ---
{cv_text}

--- JOB DESCRIPTION (JSON) ---
{job_text}

--- MATCH ANALYSIS ---
Overall score: {match_result.get("overall_score", "")}
Matched skills: {match_result.get("matched_skills", [])}
Missing skills: {match_result.get("missing_skills", [])}
Strengths: {match_result.get("strengths", [])}
Gaps: {match_result.get("gaps", [])}

==================================================
CRITICAL SKILL INJECTION RULE
==================================================

The following technologies MUST be added to:

skills.technical

{technologies_text}

STRICT RULES FOR THESE TECHNOLOGIES:
- They MUST appear inside skills.technical
- They must NOT be added to experience bullets
- They must NOT imply professional usage
- If no direct experience exists, add a qualifier such as:
  - "(basic knowledge)"
  - "(foundational)"
  - "(academic exposure)"
  - "(self-study)"
- Do NOT remove existing skills
- Do NOT duplicate skills

==================================================
GOALS
==================================================
- Improve ATS compatibility
- Increase keyword alignment
- Highlight relevant experience
- Preserve factual accuracy

==================================================
ALLOWED TRANSFORMATIONS
==================================================
- Rephrase summaries and bullet points for clarity
- Reorder skills based on relevance
- Improve professional tone
- Add the mandatory technologies listed above

==================================================
FORBIDDEN TRANSFORMATIONS
==================================================
- Inventing experience, metrics, or responsibilities
- Claiming production usage for injected technologies
- Changing job titles, employers, or dates
- Adding new roles
- Removing existing roles

==================================================
EXPERIENCE BULLET GUIDELINES
==================================================
- Start with a strong action verb
- Describe WHAT was done and HOW
- Mention impact ONLY if present in original CV
- Keep bullets concise (1–2 lines)
- Avoid vague verbs

==================================================
OUTPUT INSTRUCTIONS
==================================================
- Keep EXACTLY the same JSON structure
- Do NOT add or remove fields
- Return ONLY valid JSON
- No explanations
- No markdown
- Ensure JSON is complete

{suggestions_text}
"""

