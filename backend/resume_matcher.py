from resume_matching import match_resume_to_job

if __name__ == "__main__":
    print("JOBGUARD AI - Resume Matching")
    resume_text = input("\nPaste resume text:\n").strip()
    job_description = input("\nPaste job description:\n").strip()
    result = match_resume_to_job(resume_text, job_description)
    print("\n===== RESUME MATCHING RESULT =====")
    print("Final Match Score :", result["match_score"], "%")
    print("Semantic Score    :", result["semantic_score"], "%")
    print("Skill Score       :", result["skill_score"], "%")
    print("\nMatching Skills:")
    for skill in result["matching_skills"]:
        print("  +", skill)
    print("\nMissing Skills:")
    for skill in result["missing_skills"]:
        print("  -", skill)
