from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    KeepTogether
)
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
import os

from models import cv


# =========================
# HELPERS
# =========================
def format_date(start_month, start_year, end_month, end_year):
    start = f"{start_month}/{start_year}" if start_month and start_year else ""
    end = f"{end_month}/{end_year}" if end_month and end_year else "Present"
    return f"{start} - {end}" if start else end


# =========================
# MAIN RENDER
# =========================
def render_cv_pdf(cv, output_path: str, language: str):
    """
    Renderiza o CV em PDF. O parâmetro `language` define o idioma das seções:
    'pt' = Português, 'en' = Inglês
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Name", fontSize=18, leading=22, spaceAfter=4, fontName="Helvetica-Bold", textColor=HexColor("#111827"), alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="Header", fontSize=11, leading=13, spaceBefore=6, spaceAfter=2, fontName="Helvetica-Bold", textColor=HexColor("#1F2937")))
    styles.add(ParagraphStyle(name="Body", fontSize=9, leading=11, spaceAfter=2, textColor=HexColor("#374151")))
    styles.add(ParagraphStyle(name="Small", fontSize=8, leading=10, spaceAfter=1, textColor=HexColor("#6B7280")))

    story = []

    # =========================
    # TEXTOS POR IDIOMA
    # =========================
    titles = {
        "pt": {
            "summary": "Resumo Profissional",
            "experience": "Experiência Profissional",
            "skills": "Habilidades Técnicas",
            "education": "Formação Acadêmica",
            "certifications": "Certificações",
            "awards": "Prêmios",
            "languages": "Idiomas"
        },
        "en": {
            "summary": "Professional Summary",
            "experience": "Professional Experience",
            "skills": "Technical Skills",
            "education": "Education",
            "certifications": "Certifications",
            "awards": "Awards",
            "languages": "Languages"
        }
    }

    t = titles.get(language, titles["pt"])  # fallback para pt

    # =========================
    # HEADER
    # =========================
    pi = cv.personal_info
    story.append(Paragraph(pi.name, styles["Name"]))
    header_line = " • ".join(filter(None, [pi.location, pi.email, pi.phone, pi.linkedin, pi.github]))
    story.append(Paragraph(header_line, styles["Small"]))
    story.append(Spacer(1, 6))

    # =========================
    # SUMMARY
    # =========================
    if cv.summary:
        story.append(Paragraph(t["summary"], styles["Header"]))
        story.append(Paragraph(cv.summary, styles["Body"]))
        story.append(Spacer(1, 6))

    # =========================
    # EXPERIENCE
    # =========================
    story.append(Paragraph(t["experience"], styles["Header"]))

    MAX_EXPERIENCES = 3
    MAX_BULLETS = 3

    for exp in cv.experience[:MAX_EXPERIENCES]:
        date_range = format_date(exp.start_month, exp.start_year, exp.end_month, exp.end_year)
        bullets = [ListItem(Paragraph(item, styles["Body"])) for item in exp.description[:MAX_BULLETS]]

        story.append(
            KeepTogether([
                Paragraph(f"<b>{exp.role}</b> - {exp.company}", styles["Body"]),
                Paragraph(date_range, styles["Small"]),
                ListFlowable(bullets, bulletType="bullet", leftIndent=5),
                Spacer(1, 4)
            ])
        )

    # =========================
    # SKILLS
    # =========================
    if cv.skills and cv.skills.technical:
        story.append(Paragraph(t["skills"], styles["Header"]))
        skills_text = " | ".join(cv.skills.technical[:12])
        story.append(Paragraph(skills_text, styles["Body"]))
        story.append(Spacer(1, 4))

    # =========================
    # EDUCATION
    # =========================
    if cv.education:
        story.append(Paragraph(t["education"], styles["Header"]))
        for edu in cv.education[:3]:
            story.append(
                KeepTogether([
                    Paragraph(f"<b>{edu.field}</b> - {edu.degree}", styles["Body"]),
                    Paragraph(f"{edu.institution}", styles["Body"]),
                    Paragraph(f"{edu.start_year} - {edu.end_year}", styles["Small"]),
                    Spacer(1, 4)
                ])
            )

    # =========================
    # CERTIFICATIONS
    # =========================
    if cv.certifications:
        story.append(Spacer(1, 6))
        story.append(Paragraph(t["certifications"], styles["Header"]))
        for cert in cv.certifications[:5]:
            story.append(Paragraph(f"• {cert}", styles["Body"]))

    # =========================
    # AWARDS
    # =========================
    if cv.awards:
        story.append(Spacer(1, 6))
        story.append(Paragraph(t["awards"], styles["Header"]))
        for award in cv.awards[:5]:
            story.append(Paragraph(f"• {award}", styles["Body"]))

    # =========================
    # LANGUAGES
    # =========================
    if cv.languages:
        story.append(Spacer(1, 6))
        story.append(Paragraph(t["languages"], styles["Header"]))
        langs_text = ", ".join(cv.languages)
        story.append(Paragraph(langs_text, styles["Body"]))

    doc.build(story)
