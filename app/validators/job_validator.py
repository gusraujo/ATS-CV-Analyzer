from pydantic import ValidationError
from models.job_description import JobDescription


def validate_job(job_json: dict) -> JobDescription:
    try:
        return JobDescription.model_validate(job_json)
    except ValidationError as e:
        raise ValueError(f"Job validation failed:\n{e}")
