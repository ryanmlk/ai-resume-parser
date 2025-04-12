import torch
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from skill_classifier import SkillClassifier

# Load skill label binarizer
with open("feedback_component/models/skill_label_binarizer.pkl", "rb") as f:
    mlb = pickle.load(f)

print("✅ Loaded skill label binarizer with", len(mlb.classes_), "skills")

# === Load trained model and metadata ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load best model (adjust path as needed)
model = SkillClassifier(input_size=384, output_size=20)  # update NUM_SKILLS
model.load_state_dict(torch.load("feedback_component/models/skill_model.pth", map_location=device))
model.to(device)
model.eval()

# Load sentence transformer or define get_embedding()
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# === Inference function ===
def recommend_skills_from_summary(job_title: str, summary: str, top_k: int = 5):
    # Combine and embed input
    input_text = f"{job_title}. {summary}"
    embedding = embedder.encode(input_text)
    embedding_tensor = torch.tensor(embedding, dtype=torch.float32).to(device).unsqueeze(0)

    # Predict and extract top-k indices
    with torch.no_grad():
        outputs = model(embedding_tensor)
        topk_indices = torch.topk(outputs, top_k, dim=1).indices[0].cpu().numpy()

    # Map indices back to skill labels
    predicted_skills = [mlb.classes_[i] for i in topk_indices]
    return predicted_skills

job_title = "Data Scientist"
summary = "Experienced in analyzing large datasets, building machine learning models, and presenting insights to stakeholders."

recommended_skills = recommend_skills_from_summary(job_title, summary, top_k=5)
print("🔧 Suggested Skills:", recommended_skills)
