import re
from sentence_transformers import SentenceTransformer, util
from skill_recommender_test import recommend_skills  # This should return a list of relevant skills

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def evaluate_summary(summary: str, job_title: str, target_skills: list):
    feedback = []
    score_breakdown = {}

    # === Check 1: Summary presence ===
    if not summary or len(summary.strip()) == 0:
        return {
            "score": 0,
            "feedback": ["Summary is missing. Please add a brief professional introduction."],
            "details": {}
        }

    # === Check 2: Length ===
    sentence_count = len(re.findall(r'\.', summary))
    if sentence_count < 2:
        feedback.append("Try expanding your summary to at least 2-3 sentences.")
        score_breakdown["length"] = 0
    elif sentence_count > 4:
        feedback.append("Consider trimming your summary to keep it concise (max 3-4 lines).")
        score_breakdown["length"] = 0
    else:
        score_breakdown["length"] = 1

    # === Check 3: Buzzword detection ===
    buzzwords = ["hard-working", "motivated", "dynamic", "team player"]
    if any(word in summary.lower() for word in buzzwords):
        feedback.append("Avoid vague buzzwords like 'team player' or 'hard-working'. Focus on measurable skills or impact.")
        score_breakdown["buzzwords"] = 0
    else:
        score_breakdown["buzzwords"] = 1

    # === Check 4: Skill mention ===
    matches = [skill for skill in target_skills if skill.lower() in summary.lower()]
    if not matches:
        feedback.append(f"Consider mentioning at least one technical skill (e.g., {', '.join(target_skills[:3])}).")
        score_breakdown["skills"] = 0
    else:
        score_breakdown["skills"] = 1

    # === Check 5: Semantic match to job title ===
    similarity = util.cos_sim(model.encode(summary), model.encode(job_title))[0][0].item()
    if similarity > 0.4:
        score_breakdown["semantic_relevance"] = 1
    else:
        feedback.append(f"Make your summary more relevant to the target role '{job_title}'.")
        score_breakdown["semantic_relevance"] = 0

    # === Final score ===
    total_score = sum(score_breakdown.values())

    return {
        "score": total_score,
        "feedback": feedback,
        "details": score_breakdown,
        "matched_skills": matches,
        "semantic_similarity": round(similarity, 3)
    }

# === Example Usage ===
resume_summary = "Experienced professional with a demonstrated history of working in the tech industry. Skilled in teamwork and leadership."
target_job_title = "AI Engineer"
target_skills = recommend_skills(target_job_title, top_n=5)

result = evaluate_summary(resume_summary, target_job_title, target_skills)

print(f"\n--- Summary Evaluation for '{target_job_title}' ---")
print(f"Score: {result['score']} / 4")
print(f"Semantic Similarity: {result['semantic_similarity']}")
print("Matched Skills:", result['matched_skills'])
print("Feedback:")
for fb in result["feedback"]:
    print("-", fb)