import re
from pathlib import Path
from app.services.pdf_parser import extract_pdf_text
from app.services.docx_parser import extract_docx_text
from app.services.text_cleaner import clean_text
from app.services.section_parser import identify_sections
from app.services.skills_extractor import extract_skills
from app.utils.exceptions import ResumeParserError

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{8,}\d)(?!\d)")
LINKEDIN_RE = re.compile(r"https?://(?:www\.)?linkedin\.com/[^\s]+", re.I)
GITHUB_RE = re.compile(r"https?://(?:www\.)?github\.com/[^\s]+", re.I)

def _first(pattern, text):
    match = pattern.search(text)
    return match.group(0).strip() if match else ""

def parse_resume(path: Path) -> dict:
    ext = path.suffix.lower()
    if ext == ".pdf":
        raw = extract_pdf_text(path)
    elif ext == ".docx":
        raw = extract_docx_text(path)
    else:
        raise ResumeParserError("INVALID_FILE_TYPE", "Unsupported file format.")

    text = clean_text(raw)
    sections = identify_sections(text)
    skills = extract_skills(text)

    lines = [x.strip() for x in text.splitlines() if x.strip()]
    name = ""
    for line in lines[:8]:
        if not EMAIL_RE.search(line) and not PHONE_RE.search(line) and len(line.split()) <= 6:
            if not re.search(r"https?://|www\.|linkedin|github", line, re.I):
                name = line
                break

    return {
        "personal_information": {
            "name": name,
            "email": _first(EMAIL_RE, text),
            "phone": _first(PHONE_RE, text),
            "location": "",
            "linkedin": _first(LINKEDIN_RE, text),
            "github": _first(GITHUB_RE, text),
        },
        "summary": sections.get("summary", ""),
        "skills": {
            "technical": sorted({s for values in skills.values() for s in values}, key=str.lower),
            "by_category": skills
        },
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "projects": sections.get("projects", ""),
        "certifications": sections.get("certifications", ""),
        "languages": sections.get("languages", ""),
        "sections_detected": list(sections.keys()),
        "clean_text": text
    }
