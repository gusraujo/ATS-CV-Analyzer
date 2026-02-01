# app/api/schemas/job_input.py
from pydantic import BaseModel

class JobDescriptionInput(BaseModel):
    job_description: str