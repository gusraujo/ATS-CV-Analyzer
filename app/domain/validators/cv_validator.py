from pydantic import ValidationError
from app.domain.models.cv import CV


def validate_cv(cv_json: dict) -> CV:
    try:
        return CV.model_validate(cv_json)
    except ValidationError as e:
        raise ValueError(
            f"CV validation failed:\n{e}"
        )