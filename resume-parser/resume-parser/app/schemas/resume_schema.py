from pydantic import BaseModel
from typing import Dict, List

class PersonalInformation(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""

class ResumeData(BaseModel):
    personal_information: PersonalInformation
    summary: str = ""
    skills: Dict = {}
    education: str = ""
    experience: str = ""
    projects: str = ""
    certifications: str = ""
    languages: str = ""
    sections_detected: List[str] = []
    clean_text: str = ""
