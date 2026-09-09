from pathlib import Path
from app.utils.constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from app.utils.exceptions import ResumeParserError

def validate_upload(filename: str, content_type: str | None, content: bytes):
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ResumeParserError("INVALID_FILE_TYPE", "Only PDF and DOCX files are supported.")

    if not content:
        raise ResumeParserError("EMPTY_FILE", "The uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise ResumeParserError("FILE_TOO_LARGE", "Maximum allowed file size is 5 MB.")

    # Basic signature checks; do not trust extension alone.
    if extension == ".pdf" and not content.startswith(b"%PDF"):
        raise ResumeParserError("INVALID_PDF", "The uploaded file is not a valid PDF.")
    if extension == ".docx" and not content.startswith(b"PK"):
        raise ResumeParserError("INVALID_DOCX", "The uploaded file is not a valid DOCX package.")
