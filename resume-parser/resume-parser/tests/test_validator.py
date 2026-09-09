from app.services.file_validator import validate_upload
from app.utils.exceptions import ResumeParserError
import pytest

def test_valid_pdf_signature():
    validate_upload("resume.pdf", "application/pdf", b"%PDF-test")

def test_invalid_extension():
    with pytest.raises(ResumeParserError):
        validate_upload("resume.txt", "text/plain", b"hello")

def test_large_file():
    with pytest.raises(ResumeParserError):
        validate_upload("resume.pdf", "application/pdf", b"%PDF" + b"x" * (5 * 1024 * 1024))
