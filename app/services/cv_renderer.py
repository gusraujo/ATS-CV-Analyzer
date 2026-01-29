from jinja2 import Environment, FileSystemLoader
from pathlib import Path


def render_cv(cv, output_path: str):
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=True
    )

    template = env.get_template("cv_template.html")

    html = template.render(
        personal_info=cv.personal_info,
        summary=cv.summary,
        skills=cv.skills,
        experience=cv.experience,
        education=cv.education,
        certifications=cv.certifications,
        awards=cv.awards
    )

    Path(output_path).write_text(html, encoding="utf-8")
