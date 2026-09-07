from resume_matcher import match_resume_to_job

print("JOBGUARD AI - Member 3: Resume Matching")

resume_text = input("\nPaste resume text:\n").strip()
job_description = input("\nPaste job description:\n").strip()

result = match_resume_to_job(resume_text, job_description)

print("\n===== RESUME MATCHING RESULT =====")
print("Final Match Score :", result["match_score"], "%")
print("Semantic Score    :", result["semantic_score"], "%")
print("Skill Score       :", result["skill_score"], "%")

print("\nMatching Skills:")
for skill in result["matching_skills"]:
    print("  +", skill.title())

print("\nMissing Skills:")
for skill in result["missing_skills"]:
    print("  -", skill.title())

