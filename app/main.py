from models.cv import CV
from services.cv_renderer import render_cv_pdf
from services.match_service import run_match

from pdf_reader import read_pdf
from openai_client import extract_cv_to_json, rewrite_cv
from validators.cv_validator import validate_cv
from schemas.job_schema import JobSchema


def main():
    print("\n🚀 START ATS PIPELINE\n")

    # =========================
    # 1️⃣ READ PDF
    # =========================
    pdf_path = "examples/cv.pdf"
    print(f"📄 Reading PDF: {pdf_path}")

    resume_text = read_pdf(pdf_path)

    if not resume_text.strip():
        raise ValueError("PDF vazio ou não foi possível extrair texto")

    print("\n=== EXTRACTED PDF TEXT (FIRST 500 CHARS) ===")
    print(resume_text[:500])
    print("===========================================\n")

    # =========================
    # 2️⃣ EXTRACT CV (LLM)
    # =========================
    print("🤖 Extracting CV with OpenAI...")
    cv_raw_json = extract_cv_to_json(resume_text)

    print("\n=== RAW CV JSON FROM OPENAI ===")
    print(cv_raw_json)
    print("================================\n")

    # =========================
    # 3️⃣ VALIDATE CV
    # =========================
    print("✅ Validating CV JSON...")
    cv: CV = validate_cv(cv_raw_json)

    print("\n=== CV OBJECT AFTER VALIDATION ===")
    print("Name:", cv.personal_info.name)
    print("Email:", cv.personal_info.email)
    print("Technical skills:", cv.skills.technical)

    print("\nExperience:")
    for exp in cv.experience:
        print(
            f"- {exp.role} | {exp.company} | "
            f"{exp.start_year}–{exp.end_year}"
        )

    print("\nEducation:")
    for edu in cv.education:
        print(f"- {edu.degree} ({edu.field}) | {edu.institution}")

    print("================================\n")

    # =========================
    # 4️⃣ MOCK JOB
    # =========================
    job = JobSchema(
        title="Backend Developer",
        company="Tech Corp",
        required_skills=[
            "Java",
            "Spring Boot",
            "PostgreSQL",
            "REST API",
            "Docker"
        ],
        nice_to_have_skills=[
            "Kafka",
            "AWS",
            "Microservices"
        ],
        experience_requirements=[
            {"role": "Backend Developer", "required_years": 3},
            {"role": "Software Engineer", "required_years": 2}
        ],
        education_level="Bachelor",
        keywords=[
            "Java",
            "Spring",
            "Microservices",
            "REST",
            "Backend"
        ]
    )

    # =========================
    # 5️⃣ MATCH ENGINE
    # =========================
    print("🧠 Running ATS match engine...\n")
    match_result = run_match(cv, job)

    print("\n📊 MATCH RESULT (ORIGINAL CV)\n")
    for key, value in match_result.model_dump().items():
        print(f"{key}: {value}")

    # =========================
    # 6️⃣ REWRITE CV
    # =========================
    print("\n✍️ Rewriting CV based on match analysis...\n")

    optimized_cv_json = rewrite_cv(
        cv=cv.model_dump(),
        job=job.model_dump(),
        match_result=match_result.model_dump(),
        language="pt",
        suggestions=[
            "Quantifique resultados nas experiências, ex: 'reduzindo X% de tempo de resposta'",
            "Especifique e adicione alguns serviços AWS usados, ex: S3, EC2, Lambda",
            "Deixe claro disponibilidade para trabalho remoto se for objetivo",
            "Inclua palavras-chave do job description no resumo e nas skills técnicas",
            "Destaque projetos relevantes relacionados a backend e microservices"
        ]
    )

    optimized_cv = CV(**optimized_cv_json)

    # =========================
    # 7️⃣ RE-RUN MATCH
    # =========================
    print("\n🔁 Re-running match with optimized CV...\n")
    new_match_result = run_match(optimized_cv, job)

    print("\n📈 MATCH RESULT (OPTIMIZED CV)\n")
    for key, value in new_match_result.model_dump().items():
        print(f"{key}: {value}")

    # =========================
    # 8️⃣ RENDER PDF
    # =========================
    print("\n📄 Generating optimized CV PDF...\n")

    # Gera nome de arquivo a partir do nome do CV
    candidate_name = cv.personal_info.name.replace(" ", "_")
    output_file = f"output/CV_{candidate_name}.pdf"

    render_cv_pdf(
        cv=optimized_cv,
        output_path=output_file,
        language="pt"
    )

    print("✅ PDF gerado em output/cv_optimized.pdf")
    print("\n🏁 END ATS PIPELINE\n")


if __name__ == "__main__":
    main()
