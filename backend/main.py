"""Main JobGuard AI API."""

import json
import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

ROOT = Path(__file__).resolve().parents[1]
PARSER_ROOT = ROOT / "resume-parser" / "resume-parser"

if str(PARSER_ROOT) not in sys.path:
    sys.path.insert(0, str(PARSER_ROOT))

from app.services.resume_parser import parse_resume
from app.services.file_validator import validate_upload
from app.utils.exceptions import ResumeParserError

from resume_matching import match_resume_to_job
from fake_job_detector import analyze_job_risk


DATA_FILE = ROOT / "data" / "jobs.json"
JOBS = json.loads(DATA_FILE.read_text(encoding="utf-8"))

app = FastAPI(
    title="JobGuard AI API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "name": "JobGuard AI",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/jobs")
def jobs():
    return JOBS


@app.post("/api/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_id: int | None = Form(default=None),
    job_description: str = Form(default=""),
):
    content = await resume.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Resume file is empty."
        )

    # Validate uploaded resume
    try:
        validate_upload(
            filename=resume.filename or "",
            content_type=resume.content_type or "",
            content=content
        )
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    selected_job = None

    if job_id is not None:
        selected_job = next(
            (j for j in JOBS if j["id"] == job_id),
            None
        )

        if selected_job is None:
            raise HTTPException(
                status_code=404,
                detail="Job not found."
            )

        job_description = job_description or (
            f"{selected_job['job_title']}. "
            f"Required skills: "
            f"{', '.join(selected_job['required_skills'])}. "
            f"Project: {selected_job['project']}. "
            f"Experience: {selected_job['experience']}. "
            f"Degree: {selected_job['degree']}."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Select a job or provide a job description."
        )

    suffix = Path(
        resume.filename or "resume.pdf"
    ).suffix.lower()

    if suffix not in {".pdf", ".docx"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resumes are supported."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:
        tmp.write(content)
        temp_path = Path(tmp.name)

    try:
        # Resume parsing
        parsed = parse_resume(temp_path)

        resume_text = parsed.get(
            "clean_text",
            ""
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract readable text from resume."
            )

        # Resume-to-job matching
        required = (
            selected_job["required_skills"]
            if selected_job
            else None
        )

        matching = match_resume_to_job(
            resume_text,
            job_description,
            required_skills=required
        )

        # Job scam/risk detection
        scam = analyze_job_risk(
            job_description
        )

        return {
            "success": True,
            "job": selected_job,
            "resume": parsed,
            "matching": matching,
            "scam_risk": scam,
        }

    except ResumeParserError as exc:
        raise HTTPException(
            status_code=400,
            detail={
                "code": exc.code,
                "message": str(exc)
            }
        )

    finally:
        temp_path.unlink(
            missing_ok=True
        )
