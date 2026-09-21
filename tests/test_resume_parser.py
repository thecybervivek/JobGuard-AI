from app.services.section_parser import identify_sections
from app.services.skills_extractor import extract_skills

def test_sections():
    result = identify_sections("John Doe\n\nSKILLS\nPython\nDjango\n\nEDUCATION\nDiploma")
    assert result["skills"] == "Python\nDjango"
    assert result["education"] == "Diploma"

def test_skills():
    result = extract_skills("Python Django HTML MySQL")
    assert "Python" in result["programming"]
    assert "Django" in result["backend"]
