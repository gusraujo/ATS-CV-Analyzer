from fastapi import FastAPI
from app.api.routes import job_routes, cv_routes, process_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ATS API")

app.include_router(job_routes.router)
app.include_router(cv_routes.router)
app.include_router(process_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4200",
        "https://ats-analyzer-5bf88.web.app",
        "https://ats-analyzer-5bf88.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}