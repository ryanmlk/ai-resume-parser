import pandas as pd
import numpy as np
import requests
from pymongo import MongoClient
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from collections import Counter
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import ast
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score
import copy
from skill_classifier import SkillClassifier
import spacy
from sentence_transformers import SentenceTransformer

# --- LMStudio CONFIG ---
API_URL = "http://127.0.0.1:1234/v1/embeddings"
EMBEDDING_DIM = 768

# # --- 1. Connect to MongoDB ---
# client = MongoClient("mongodb://localhost:27017/")
# db = client["jobs_data"]
# collection = db["jobs"]

# # --- 2. Load data from MongoDB ---
# print("Fetching job data from MongoDB...")
# data = list(collection.find(
#     {"core_position": {"$exists": True}, "core_skills": {"$exists": True, "$ne": []}},
#     {"core_position": 1, "core_skills": 1, "text": 1, "_id": 0}
# ))
# df = pd.DataFrame(data)

# # --- 3. Clean skill lists ---
# print("Cleaning skill lists...")
# nlp = spacy.load("en_core_web_sm")
# def clean_skills(skill_list):
#     if not isinstance(skill_list, list):
#         return []
#     cleaned_skills = []
#     for skill in skill_list:
#         if isinstance(skill, str):
#             doc = nlp(skill.lower().strip())
#             for token in doc:
#                 if token.pos_ in ['NOUN', 'PROPN']:
#                     cleaned_skills.append(token.text)
#     return cleaned_skills

# df["core_skills_cleaned"] = df["core_skills"].apply(clean_skills)

# # --- 4. Filter rare skills (keep skills used in ≥10 jobs) ---
# print("Filtering rare skills...")
# flat_skills = [s for sublist in df["core_skills_cleaned"] for s in sublist]
# skill_counts = Counter(flat_skills)
# common_skills = set([s for s, count in skill_counts.items() if count >= 10])

# df["filtered_skills"] = df["core_skills_cleaned"].apply(lambda skills: [s for s in skills if s in common_skills])
# df = df[df["filtered_skills"].str.len() > 0]  # Drop rows with no common skills
# df.to_csv("feedback_component/cleaned_job_data.csv", index=False)
df = pd.read_csv("feedback_component/cleaned_job_data.csv")

# --- 5. Embed job titles using LM Studio ---
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

def get_avg_embedding(text, chunk_size=300):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = [get_embedding(chunk) for chunk in chunks]
    return np.mean(embeddings, axis=0)

X = np.stack(
    df.apply(lambda row: get_avg_embedding(f"{row['core_position']}. {row['text']}"), axis=1)
)
with open("feedback_component/models/job_title_embeddings.npy", "wb") as f:
    np.save(f, X)

# print("Generating embeddings for job titles...")
# X = np.stack(df["core_position"].apply(get_embedding))
# with open("backend/feedback_component/job_title_embeddings.npy", "wb") as f:
#     np.save(f, X)

# Load cleaned skills if not in memory already
df["filtered_skills"] = df["filtered_skills"].apply(ast.literal_eval)

# Flatten and count
print("Counting skills...")
flat_skills = [skill for sublist in df["filtered_skills"] for skill in sublist]
skill_counts = Counter(flat_skills)

# Get top N skills (optional)
top_skills = [s for s, count in skill_counts.items()]

print("Generating embeddings for skills...")
model = SentenceTransformer("all-MiniLM-L6-v2")
skill_embeddings = model.encode(top_skills)

print("Clustering skills...")
dbscan = DBSCAN(eps=0.3, min_samples=2, metric="cosine")
labels = dbscan.fit_predict(skill_embeddings)

# Create mapping
print("Creating mappping...")
skill_cluster_df = pd.DataFrame({"skill": top_skills, "cluster": labels})

canonical_map = {}
grouped = skill_cluster_df.groupby("cluster")["skill"]

for cluster_id, group in grouped:
    if cluster_id == -1:  # noise, skip or keep as-is
        for skill in group:
            canonical_map[skill] = skill
    else:
        # Use most frequent term or the first one
        canonical_skill = group.iloc[0]
        for skill in group:
            canonical_map[skill] = canonical_skill

standardized_skills = []
for skill_list in df["filtered_skills"]:
    clean = [canonical_map.get(s, s) for s in skill_list]
    standardized_skills.append(clean)

# # --- 6. Multi-label encode skills ---
print("Multi-label encoding skills...")
mlb = MultiLabelBinarizer()
Y = mlb.fit_transform(standardized_skills)

# Save the encoded skills matrix Y
with open("feedback_component/models/skill_encoded_matrix.npy", "wb") as f:
    np.save(f, Y)
with open('feedback_component/skill_label_binarizer.pkl', 'wb') as f:
    pickle.dump(mlb, f)
print(mlb.classes_)
print("✅ Saved skill label binarizer with", len(mlb.classes_), "skills")

# X = np.load("feedback_component/models/job_title_embeddings.npy")
# Y = np.load("backend/feedback_component/models/skill_encoded_matrix.npy")

# Convert data
X_tensor = torch.tensor(X, dtype=torch.float32)
Y_tensor = torch.tensor(Y, dtype=torch.float32)

# Train/test split
X_train, X_test, Y_train, Y_test = train_test_split(X_tensor, Y_tensor, test_size=0.2, random_state=42)

# Send to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
X_train, Y_train = X_train.to(device), Y_train.to(device)

model = SkillClassifier(X.shape[1], Y.shape[1]).to(device)

# Train
optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-5)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
loss_fn = nn.BCELoss()

best_f1 = 0.0
patience = 5
wait = 0
best_model_state = None

for epoch in range(50):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = loss_fn(outputs, Y_train)
    loss.backward()
    optimizer.step()
    scheduler.step()

    # Validation F1 (Top-K = 5 by default for early stopping)
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_test)
        preds = torch.zeros_like(val_outputs)
        topk_indices = torch.topk(val_outputs, 5, dim=1).indices
        for i, row in enumerate(topk_indices):
            preds[i, row] = 1

    f1 = f1_score(Y_test.cpu(), preds.cpu(), average="micro")

    # Early stopping
    if f1 > best_f1:
        best_f1 = f1
        wait = 0
        best_model_state = copy.deepcopy(model.state_dict())
    else:
        wait += 1
        if wait >= patience:
            print(f"⏹️ Early stopping triggered at epoch {epoch+1}.")
            break

print(f"✅ Best F1 (Top-K=5): {best_f1:.4f}")

# Save best model
model_path = f"feedback_component/models/skill_model.pth"
torch.save(best_model_state, model_path)
print(f"📦 Model saved to {model_path}")

# Load best model for final Top-K evaluations
model.load_state_dict(torch.load(model_path))
model.eval()

for top_k in [3, 5]:
    with torch.no_grad():
        outputs = model(X_test)
        preds = torch.zeros_like(outputs)
        topk_indices = torch.topk(outputs, top_k, dim=1).indices
        for i, row in enumerate(topk_indices):
            preds[i, row] = 1

    f1 = f1_score(Y_test.cpu(), preds.cpu(), average="micro")
    precision = precision_score(Y_test.cpu(), preds.cpu(), average="micro")
    recall = recall_score(Y_test.cpu(), preds.cpu(), average="micro")

    print(f"\n📊 Top K: {top_k}")
    print(f"F1 (micro): {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")

# === Inference function ===
def recommend_skills_from_summary(job_title: str, summary: str, top_k: int = 5):
    # Combine and embed input
    input_text = f"{job_title}. {summary}"
    embedding = get_embedding(input_text)
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


