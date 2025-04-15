import re
from sentence_transformers import SentenceTransformer, util
# from skill_recommender_test import recommend_skills  # This should return a list of relevant skills
from feedback_component import skill_model

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

buzzwords = [
    "team player", "hard-working", "motivated", "self-starter", "go-getter",
    "dynamic", "passionate", "dedicated", "results-driven", "fast learner",
    "responsible", "proactive", "detail-oriented", "synergistic",
    "enthusiastic", "excellent communication skills", "innovative thinker",
    "outside the box", "strategic", "creative", "visionary", "thought leader",
    "multi-tasker", "problem solver", "solution-oriented", "collaborative",
    "empowered", "committed", "reliable", "growth mindset"
]


def evaluate_summary(summary: str, job_title: str = None, target_skills: list = None):
    feedback = []
    score = 0
    max_points = 4
    score_breakdown = {}

    # === Check 1: Summary presence ===
    if not summary or len(summary.strip()) == 0:
        feedback.append("Summary is missing. Please add a brief professional introduction.")
        return {"score": 0.0, "feedback": feedback}

    # === Check 2: Length ===
    sentence_count = len(re.findall(r'\.', summary))
    if sentence_count < 2:
        feedback.append("Try expanding your summary to at least 2-3 sentences.")
        score += 0.5
    elif sentence_count > 4:
        feedback.append("Consider trimming your summary to keep it concise (max 3-4 lines).")
        score += 0.5
    else:
        score += 1

    # === Check 3: Buzzword detection ===
    buzzwords_found = [word for word in buzzwords if word.lower() in summary.lower()]
    if buzzwords_found:
        buzzword_examples = ", ".join([f"'{word}'" for word in buzzwords_found[:3]])
        if len(buzzwords_found) > 3:
            buzzword_examples += f" and {len(buzzwords_found)-3} more"
        feedback.append(f"Avoid vague buzzwords like {buzzword_examples}. Focus on measurable skills or impact instead.")
        score += 0.5
    else:
        score += 1

    # === Check 4: Skill mention ===
    if target_skills:
        matches = [skill for skill in target_skills if skill.lower() in summary.lower()]
        if not matches:
            feedback.append(f"Consider mentioning at least one technical skill (e.g., {', '.join(target_skills[:3])}).")
            score += 0.3
        elif len(matches) < 2:
            feedback.append(f"Good! But consider adding more skills like {', '.join(target_skills[3:6])}.")
            score += 0.5
        else:
            score += 1

    # === Check 5: Semantic match to job title ===
    if job_title:
        similarity = util.cos_sim(model.encode(summary), model.encode(job_title))[0][0].item()
        if similarity > 0.4:
            score += 1
        else:
            feedback.append(f"Make your summary more relevant to the target role '{job_title}'.")
            score += 0.5

    # === Final score ===
    return {
        "score": round(score / max_points, 2),
        "feedback": feedback
    }
    
def evaluate_personal_info(data: dict):
    feedback = []
    section_score = 0
    max_section_points = 5

    # Each item contributes 1 point
    if data.get("name") and len(data["name"].split()) >= 2:
        section_score += 1
    else:
        feedback.append("Your full name should be provided.")

    email = data.get("email", "")
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        section_score += 1
    else:
        feedback.append("Email address is missing or invalid.")

    phone = data.get("phone", "")
    if re.search(r"\+?\d[\d\s\-()]{6,}", phone):
        section_score += 1
    else:
        feedback.append("Phone number is missing or invalid.")

    if data.get("linkedin_url"):
        section_score += 1
    else:
        feedback.append("Consider adding a LinkedIn profile to boost credibility.")

    if data.get("portfolio_url") or data.get("github_url") or data.get("other_links"):
        section_score += 1
    else:
        feedback.append("Consider adding a portfolio or GitHub link.")

    return {
        "score": section_score / max_section_points,  # score between 0 and 1
        "feedback": feedback
    }

def evaluate_work_experience(work: list, target_skills: list = None):
    if not work:
        return {"score": 0.0, "feedback": ["No work experience found."]}

    total_score = 0
    feedback = []

    for i, entry in enumerate(work):
        entry_score = 0
        issues = []

        # Check for title, company, and location
        if all(entry.get(k) for k in ["job_title", "company", "location"]):
            entry_score += 1
        else:
            issues.append("missing job title, company, or location")

        # Check description
        desc = (entry.get("description") or "").strip()
        if len(desc.split()) >= 10:
            entry_score += 1
        else:
            issues.append("description is too short or missing")

        # Check for skill mentions
        if target_skills:
            matches = [skill for skill in target_skills if skill.lower() in entry.get("description", "").lower()]
            if not matches:
                issues.append(f"Consider mentioning at least one technical skill (e.g., {', '.join(target_skills[:3])})")
                entry_score += 0.3
            elif len(matches) < 2:
                issues.append(f"Good! But consider adding more skills like {', '.join(target_skills[3:6])}.")
                entry_score += 0.5
            else:
                entry_score += 1

        max_entry_score = 4 if target_skills else 3
        total_score += entry_score / max_entry_score

        if issues:
            feedback.append(f"Experience {i+1}: " + "; ".join(issues))

    normalized_score = total_score / len(work)
    return {
        "score": round(normalized_score, 2),
        "feedback": feedback
    }

def evaluate_education(edu: list):
    if not edu:
        return {"score": 0, "feedback": ["No education history found."]}
    return {"score": 1, "feedback": ["Education section looks good."]}

def evaluate_skills(skills: list):
    if not skills:
        return {"score": 0, "feedback": ["No skills found. Add relevant technical or soft skills."]}
    if len(skills) < 5:
        return {"score": 0.5, "feedback": ["Consider adding more skills relevant to the job."]}
    return {"score": 1, "feedback": ["Skills section is well populated."]}

def evaluate_resume(parsed_resume: dict):
    target_skills = skill_model.recommend_skills_from_summary(parsed_resume.get("job_title", ""), parsed_resume.get("summary", ""), top_k=5)
    personal = evaluate_personal_info(parsed_resume.get("personal_information", {}))
    summary = evaluate_summary(parsed_resume.get("summary", ""), "", target_skills)
    experience = evaluate_work_experience(parsed_resume.get("work_experience", []), target_skills)
    education = evaluate_education(parsed_resume.get("education", []))
    skills = evaluate_skills(parsed_resume.get("skills", []))

    final_score = (
        personal["score"] * 10 +
        summary["score"] * 20 +
        experience["score"] * 30 +
        education["score"] * 20 +
        skills["score"] * 20
    )

    return {
        "score": round(final_score, 1),
        "sections": {
            "personal_information": personal,
            "summary": summary,
            "work_experience": experience,
            "education": education,
            "skills": skills
        }
    }




# # === Example Usage ===
# resume_summary = "Experienced professional with a demonstrated history of working in the tech industry. Skilled in teamwork and leadership."
# target_job_title = "AI Engineer"
# target_skills = recommend_skills(target_job_title, top_n=5)

# result = evaluate_summary(resume_summary, target_job_title, target_skills)

# print(f"\n--- Summary Evaluation for '{target_job_title}' ---")
# print(f"Score: {result['score']} / 4")
# print(f"Semantic Similarity: {result['semantic_similarity']}")
# print("Matched Skills:", result['matched_skills'])
# print("Feedback:")
# for fb in result["feedback"]:
#     print("-", fb)