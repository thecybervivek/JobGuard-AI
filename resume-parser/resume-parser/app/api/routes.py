import time
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.file_validator import validate_upload
from app.services.resume_parser import parse_resume
from app.utils.exceptions import ResumeParserError
from app.utils.constants import UPLOAD_DIR

router = APIRouter(tags=["Resume Parser"])

@router.post("/resume/parse")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    start = time.perf_counter()
    try:
        content = await file.read()
        validate_upload(file.filename or "", file.content_type, content)

        safe_name = Path(file.filename).name
        saved_path = UPLOAD_DIR / safe_name
        saved_path.write_bytes(content)

        result = parse_resume(saved_path)

        result["metadata"] = {
            "file_name": safe_name,
            "file_type": saved_path.suffix.lower(),
            "file_size_bytes": len(content),
            "processing_time_ms": round((time.perf_counter() - start) * 1000, 2)
        }
        return {"success": True, "data": result}

    except ResumeParserError as exc:
        raise HTTPException(status_code=400, detail={
            "success": False, "error": {"code": exc.code, "message": str(exc)}
        })
    except Exception:
        raise HTTPException(status_code=500, detail={
            "success": False, "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred while parsing the resume."
            }
        })
