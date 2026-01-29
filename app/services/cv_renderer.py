from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
import os


def format_date(start_month, start_year, end_month, end_year):
    start = f"{start_month}/{start_year}" if start_month and start_year else ""
    end = (
        f"{end_month}/{end_year}"
        if end_month and end_year
        else "Atual"
    )

    if start:
        return f"{start} – {end}"
    return end


def render_cv_pdf(cv, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="Name",
        fontSize=20,
        spaceAfter=12,
        textColor=HexColor("#1F2937"),
        leading=22
    ))

    styles.add(ParagraphStyle(
        name="Header",
        fontSize=12,
        spaceAfter=6,
        textColor=HexColor("#111827"),
        leading=14,
        fontName="Helvetica-Bold"
    ))

    styles.add(ParagraphStyle(
        name="Body",
        fontSize=10,
        spaceAfter=6,
        leading=14,
        textColor=HexColor("#374151")
    ))

    styles.add(ParagraphStyle(
        name="Small",
        fontSize=9,
        spaceAfter=4,
        leading=12,
        textColor=HexColor("#6B7280")
    ))

    story = []

    # =========================
    # HEADER
    # =========================
    pi = cv.personal_info
    story.append(Paragraph(pi.name, styles["Name"]))
    story.append(Paragraph(
        f"{pi.headline} • {pi.location} • {pi.email} • {pi.phone}",
        styles["Small"]
    ))
    story.append(Spacer(1, 12))

    # =========================
    # SUMMARY
    # =========================
    story.append(Paragraph("Resumo Profissional", styles["Header"]))
    story.append(Paragraph(cv.summary, styles["Body"]))
    story.append(Spacer(1, 12))

    # =========================
    # EXPERIENCE
    # =========================
    story.append(Paragraph("Experiência Profissional", styles["Header"]))

    for exp in cv.experience:
        story.append(Paragraph(
            f"{exp.role} — {exp.company}",
            styles["Body"]
        ))

        date_range = format_date(
            exp.start_month,
            exp.start_year,
            exp.end_month,
            exp.end_year
        )

        story.append(Paragraph(
            date_range,
            styles["Small"]
        ))

        bullets = [
            ListItem(Paragraph(item, styles["Body"]))
            for item in exp.description
        ]

        story.append(ListFlowable(
            bullets,
            bulletType="bullet",
            leftIndent=12
        ))

        story.append(Spacer(1, 10))


    # =========================
    # EDUCATION
    # =========================
    story.append(Paragraph("Formação Acadêmica", styles["Header"]))

    for edu in cv.education:
        story.append(Paragraph(
            f"{edu.degree} — {edu.institution}",
            styles["Body"]
        ))
        story.append(Paragraph(
            f"{edu.start_year} – {edu.end_year}",
            styles["Small"]
        ))
        story.append(Spacer(1, 6))

    # =========================
    # AWARDS (OPCIONAL)
    # =========================
    if cv.awards:
        story.append(Spacer(1, 12))
        story.append(Paragraph("Certificações & Prêmios", styles["Header"]))

        for award in cv.awards:
            story.append(Paragraph(f"• {award}", styles["Body"]))

    doc.build(story)