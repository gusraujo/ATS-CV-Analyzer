from fastapi import FastAPI
from app.api.routes import job_routes, cv_routes, process_routes

app = FastAPI(title="ATS API")

app.include_router(job_routes.router)
app.include_router(cv_routes.router)
app.include_router(process_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}