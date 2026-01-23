from openai_client import extract_cv_to_json
from pdf_reader import read_pdf
from validators.cv_validator import validate_cv

def main():
    resume_text = read_pdf("examples/cv.pdf")

    cv_json = extract_cv_to_json(resume_text)

    cv = validate_cv(cv_json)

    print("===== VALIDATED CV OBJECT =====")
    print(cv)

    print("\nCandidate name:", cv.personal_info.name)
    print("Skills:", cv.skills["technical"])

if __name__ == "__main__":
    main()

