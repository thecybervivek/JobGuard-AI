import re

ALIASES = {
    "summary": ["summary", "profile", "professional summary", "career objective", "objective"],
    "skills": ["skills", "technical skills", "technical expertise", "core skills"],
    "education": ["education", "educational background", "academic qualification", "qualifications"],
    "experience": ["experience", "work experience", "professional experience", "employment history"],
    "projects": ["projects", "personal projects", "academic projects"],
    "certifications": ["certifications", "certificates", "licenses & certifications"],
    "languages": ["languages", "language proficiency"],
}

def _canonical_heading(line):
    normalized = re.sub(r"[^a-z0-9& ]", "", line.lower()).strip()
    for key, aliases in ALIASES.items():
        if normalized in aliases:
            return key
    return None

def identify_sections(text: str) -> dict:
    sections = {}
    current = "header"
    sections[current] = []
    for line in text.splitlines():
        heading = _canonical_heading(line)
        if heading:
            current = heading
            sections.setdefault(current, [])
        else:
            sections.setdefault(current, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}
