from models.cv import CV
from pydantic import ValidationError


def validate_cv(cv_json: dict) -> CV:
    try:
        return CV.model_validate(cv_json)
    except ValidationError as e:
        raise ValueError(
            f"CV validation failed:\n{e}"
        )