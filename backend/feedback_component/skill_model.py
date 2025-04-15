import joblib
import numpy as np
import requests
import torch
from feedback_component import skill_classifier

API_URL = "http://127.0.0.1:1234/v1/embeddings"
EMBEDDING_DIM = 768

def get_embedding(text):
    payload = {
        "input": text,
        "model": "text-embedding-nomic-embed-text-v1.5"
    }
    try:
        response = requests.post(API_URL, json=payload).json()
        return np.array(response["data"][0]["embedding"])
    except Exception as e:
        print(f"Error embedding '{text}': {e}")
        return np.zeros(EMBEDDING_DIM)

mlb = joblib.load('feedback_component/models/skill_label_binarizer.joblib')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "feedback_component/models/skill_model.pth"
skill_classifier_model = skill_classifier.SkillClassifier(input_size=EMBEDDING_DIM, output_size=len(mlb.classes_)).to(device)

# Load the saved weights
skill_classifier_model.load_state_dict(torch.load(model_path, map_location=device))
skill_classifier_model.eval()

def recommend_skills_from_summary(job_title: str, summary: str, top_k: int = 6):
    # Combine and embed input
    input_text = f"{job_title}. {summary}"
    embedding = get_embedding(input_text)
    embedding_tensor = torch.tensor(embedding, dtype=torch.float32).to(device).unsqueeze(0)

    # Predict and extract top-k indices
    with torch.no_grad():
        outputs = skill_classifier_model(embedding_tensor)
        topk_indices = torch.topk(outputs, top_k, dim=1).indices[0].cpu().numpy()

    # Map indices back to skill labels
    predicted_skills = [mlb.classes_[i] for i in topk_indices]
    return predicted_skills