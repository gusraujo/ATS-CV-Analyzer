from services.cv_renderer import render_cv_pdf
from pdf_reader import read_pdf
from openai_client import extract_cv_to_json
from validators.cv_validator import validate_cv
from schemas.job_schema import JobSchema
from services.match_service import run_match


def main():
    print("\n🚀 START ATS PIPELINE\n")

    # 1️⃣ Ler o PDF
    pdf_path = "examples/cv.pdf"
    print(f"📄 Reading PDF: {pdf_path}")

    resume_text = read_pdf(pdf_path)

    print("\n=== EXTRACTED PDF TEXT (FIRST 500 CHARS) ===")
    print(resume_text[:500])
    print("===========================================\n")

    if not resume_text.strip():
        raise ValueError("PDF vazio ou não foi possível extrair texto")

    # 2️⃣ Extrair CV com OpenAI
    print("🤖 Sending resume to OpenAI for extraction...")
    cv_raw_json = extract_cv_to_json(resume_text)

    print("\n=== RAW CV JSON FROM OPENAI ===")
    print(cv_raw_json)
    print("================================\n")

    # 3️⃣ Validar CV (Pydantic)
    print("✅ Validating CV JSON with Pydantic...")
    cv = validate_cv(cv_raw_json)

    print("\n=== CV OBJECT AFTER VALIDATION ===")
    print("Name:", cv.personal_info.name)
    print("Email:", cv.personal_info.email)
    print("Skills:", cv.skills)

    print("\nExperience:")
    for exp in cv.experience:
        print(
            f"- Role: {exp.role} | Company: {exp.company} | "
            f"Period: {exp.start_year}-{exp.end_year}"
        )

    print("\nEducation:")
    for edu in cv.education:
        print(f"- Degree: {edu.degree} | Field: {edu.field}")

    print("================================\n")

    # 4️⃣ Mock de vaga
    job = JobSchema(
        title="Backend Developer",
        company="Tech Corp",
        required_skills=[
            "Java", "Spring Boot", "PostgreSQL",
            "REST API", "Docker"
        ],
        nice_to_have_skills=[
            "Kafka", "AWS", "Microservices"
        ],
        experience_requirements=[
            {"role": "Backend Developer", "required_years": 3},
            {"role": "Software Engineer", "required_years": 2}
        ],
        education_level="Bachelor",
        keywords=["Java", "Spring", "Microservices"]
    )

    print("\n=== JOB DESCRIPTION (INPUT TO MATCH) ===")
    print("Title:", job.title)
    print("Company:", job.company)
    print("Required skills:", job.required_skills)
    print("Nice to have:", job.nice_to_have_skills)
    print("Keywords:", job.keywords)
    print("=======================================\n")

    # 5️⃣ Executar Match
    print("🧠 Running ATS match engine...\n")
    match_result = run_match(cv, job)

    # 6️⃣ Output (Pydantic-safe)
    print("\n📊 RESULTADO DO MATCH ATS\n")

    result_dict = match_result.model_dump()

    for key, value in result_dict.items():
        print(f"{key}: {value}")

    print("\n🏁 END PIPELINE\n")
    
    render_cv_pdf(
    cv=cv,
    output_path="output/cv_rendered.pdf"
    )

    print("📄 Currículo PDF gerado em output/cv_rendered.pdf")


if __name__ == "__main__":
    main()
