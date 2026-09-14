"""Resume-to-job matching module."""

import re
from functools import lru_cache
from typing import Iterable

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "all-MiniLM-L6-v2"

SKILL_ALIASES = {
    "ml": "machine learning",
    "ai/ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
    "js": "javascript",
    "ts": "typescript",
    "react": "react.js",
    "reactjs": "react.js",
    "node": "node.js",
    "sklearn": "scikit-learn",
    "rest": "rest api",
}


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def _normalise(text: str) -> str:
    text = text.lower()
    for old, new in SKILL_ALIASES.items():
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    return re.sub(r"\s+", " ", text).strip()


def _skill_set(skills: Iterable[str]) -> set[str]:
    return {_normalise(s) for s in skills if s and s.strip()}


def _contains_skill(resume: str, skill: str) -> bool:
    skill = _normalise(skill)
    resume = _normalise(resume)
    return skill in resume


def match_resume_to_job(
    resume_text: str,
    job_description: str,
    required_skills=None
) -> dict:
    """Return semantic score, skill score, final score and skill gap."""

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    if not resume_text or not job_description:
        raise ValueError("Resume text and job description are required.")

    model = get_model()

    embeddings = model.encode(
        [resume_text, job_description],
        normalize_embeddings=True
    )

    semantic_score = float(
        cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0] * 100
    )

    semantic_score = max(0.0, min(100.0, semantic_score))

    if required_skills:
        skills = list(required_skills)
    else:
        skills = []

        common = [
            "python", "java", "javascript", "typescript",
            "react.js", "angular", "vue.js", "django",
            "flask", "fastapi", "sql", "mongodb", "git",
            "github", "aws", "pandas", "numpy", "pytorch",
            "tensorflow", "keras", "scikit-learn",
            "machine learning", "deep learning", "nlp",
            "computer vision", "generative ai", "langchain",
            "llamaindex", "rest api", "html5", "css3",
            "node.js", "next.js", "react native", "docker",
            "dsa", "statistics"
        ]

        jd = _normalise(job_description)
        skills = [s for s in common if s in jd]

    matched = [
        s for s in skills
        if _contains_skill(resume_text, s)
    ]

    missing = [
        s for s in skills
        if not _contains_skill(resume_text, s)
    ]

    skill_score = (
        len(matched) / len(skills) * 100
        if skills else 0.0
    )

    final_score = (
        semantic_score * 0.70
        + skill_score * 0.30
    )

    return {
        "match_score": round(final_score, 2),
        "semantic_score": round(semantic_score, 2),
        "skill_score": round(skill_score, 2),
        "matching_skills": matched,
        "missing_skills": missing,
    }


match_resume = match_resume_to_job
