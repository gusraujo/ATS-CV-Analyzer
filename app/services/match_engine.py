from typing import List, Dict


def normalize(text: str) -> str:
    return text.lower().strip()


# =========================
# SKILLS MATCH
# =========================
def match_skills(
    cv_skills: List[str],
    job_skills: List[str],
    skill_aliases: Dict[str, List[str]]
) -> Dict:
    cv_norm = [normalize(s) for s in cv_skills]

    matched = []
    missing = []
    matched_details = {}

    for job_skill in job_skills:
        job_norm = normalize(job_skill)

        aliases = skill_aliases.get(job_norm, [])
        search_terms = [job_norm] + aliases

        found_terms = []

        for cv_skill in cv_norm:
            for term in search_terms:
                if term in cv_skill:
                    found_terms.append(term)

        if found_terms:
            matched.append(job_skill)
            matched_details[job_skill] = list(set(found_terms))
        else:
            missing.append(job_skill)

    score = round((len(matched) / len(job_skills)) * 100, 2) if job_skills else 100

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "details": matched_details,
        "justification": f"{len(matched)} de {len(job_skills)} skills obrigatórias encontradas"
    }



# =========================
# EXPERIENCE MATCH
# =========================
def match_experience(cv_experiences, job_requirements) -> Dict:
    matched_roles = []
    total_years = 0

    for req in job_requirements:
        req_role = normalize(req.role)

        for exp in cv_experiences:
            exp_role = normalize(exp.role)

            if req_role in exp_role or exp_role in req_role:
                matched_roles.append(exp.role)
                total_years += getattr(exp, "years", 1)
                break

    if not job_requirements:
        return {
            "score": 100,
            "matched_roles": [],
            "years_considered": 0,
            "justification": "Nenhum requisito de experiência definido"
        }

    score = min((total_years / 5) * 100, 100)
    score = round(score, 2)

    return {
        "score": score,
        "matched_roles": matched_roles,
        "years_considered": total_years,
        "justification": (
            f"{total_years} anos de experiência relevante identificados"
            if total_years > 0
            else "Nenhuma experiência relevante identificada"
        )
    }



# =========================
# EDUCATION MATCH
# =========================
def match_education(cv_education, required_level: str) -> Dict:
    if not required_level:
        return {
            "score": 100,
            "degree": None,
            "justification": "Nenhum requisito educacional definido"
        }

    for edu in cv_education:
        if normalize(required_level) in normalize(edu.degree):
            return {
                "score": 100,
                "degree": edu.degree,
                "justification": "Nível educacional atende ao requisito"
            }

    return {
        "score": 40,
        "degree": cv_education[0].degree if cv_education else None,
        "justification": "Nível educacional abaixo do desejado, mas aceitável"
    }
