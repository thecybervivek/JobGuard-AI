# Resume Parser API

A modular Resume Parser supporting PDF and DOCX files with validation, file-size limits, text cleaning, section detection, skill extraction, structured JSON output, and FastAPI endpoints.

## Features

- PDF validation
- DOCX support
- 5 MB file-size limit
- Clear API error handling
- PDF text extraction with `pdfplumber`
- DOCX text extraction with `python-docx`
- Text cleaning
- Resume section identification
- Skills extraction from a configurable `skills.json`
- Structured JSON response
- FastAPI + Swagger/OpenAPI
- Basic pytest test suite

## Setup on Windows / VS Code

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then activate again.

## Run

```powershell
uvicorn app.main:app --reload
```

Open:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## API

`POST /api/v1/resume/parse`

Upload a `.pdf` or `.docx` file using the `file` form field.

Example response:

```json
{
  "success": true,
  "data": {
    "personal_information": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+91 9876543210",
      "location": "",
      "linkedin": "",
      "github": ""
    },
    "summary": "",
    "skills": {
      "technical": ["Django", "HTML", "Python"],
      "by_category": {
        "programming": ["Python"],
        "frontend": ["HTML"],
        "backend": ["Django"]
      }
    },
    "education": "Diploma in Information Technology",
    "experience": "",
    "projects": "",
    "certifications": "",
    "languages": "",
    "sections_detected": ["header", "skills", "education"],
    "clean_text": "..."
  }
}
```

## Tests

```powershell
pytest -q
```

## Notes

This version intentionally uses deterministic parsing rather than an LLM. For scanned/image-only PDFs, add an OCR layer later. For production deployment, add authentication, rate limiting, filename collision handling, virus scanning, secure temporary storage, and automatic deletion of uploaded files.
