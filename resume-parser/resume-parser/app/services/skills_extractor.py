import json
import re
from pathlib import Path

SKILLS_FILE = Path(__file__).resolve().parents[1] / "data" / "skills.json"

def load_skills():
    return json.loads(SKILLS_FILE.read_text(encoding="utf-8"))

def extract_skills(text: str) -> dict:
    catalog = load_skills()
    found = {}
    lower = text.lower()
    for category, skills in catalog.items():
        matches = []
        for skill in skills:
            pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
            if re.search(pattern, lower):
                matches.append(skill)
        if matches:
            found[category] = sorted(set(matches), key=str.lower)
    return found
