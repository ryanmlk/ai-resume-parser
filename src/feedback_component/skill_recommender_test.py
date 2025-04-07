import requests
import pandas as pd
from pymongo import MongoClient
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from sentence_transformers import SentenceTransformer
import pickle

# LM Studio API endpoint for embeddings
API_URL = "http://127.0.0.1:1234/v1/embeddings"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["jobs_data"]
collection = db["jobs"]

# Fetch data from MongoDB
data = list(collection.find(
    {"core_position": {"$exists": True}, "core_skills": {"$exists": True, "$ne": []}},
    {"core_position": 1, "core_skills": 1, "_id": 1}
))
df = pd.DataFrame(data)

# Split into train and test sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
skill_lists_train = train_df["core_skills"].tolist()

# Load the trained KNN model
def load_knn_model(model_path='src/feedback_component/skill_predictor.pkl'):
    try:
        with open(model_path, 'rb') as f:
            loaded_model = pickle.load(f)
        print(f"KNN model loaded successfully from {model_path}")
        return loaded_model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

knn = load_knn_model()
if knn is None:
    print("Falling back to training a new model...")
    # knn = NearestNeighbors(n_neighbors=10, metric="cosine").fit(X_train)

def get_embedding(text):
    payload = {
        "input": text,
        "model": "nomic-embed-text"
    }
    try:
        response = requests.post(API_URL, json=payload).json()
        return np.array(response["data"][0]["embedding"])
    except Exception as e:
        print(f"Error embedding '{text}': {e}")
        return np.zeros(384)  # Fallback embedding (adjust size based on LLaMA output)

def recommend_skills(job_title, top_n):
    embedding = get_embedding(job_title)
    distances, indices = knn.kneighbors([embedding], n_neighbors=top_n)
    skills = [skill for idx in indices[0] for skill in skill_lists_train[idx]]
    return list(dict.fromkeys(skills))[:top_n]

# Evaluation functions
def precision_recall_f1(recommended, true):
    recommended_set = set(recommended)
    true_set = set(true)
    intersection = recommended_set & true_set
    precision = len(intersection) / len(recommended) if recommended else 0
    recall = len(intersection) / len(true) if true else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

def average_precision(recommended, true):
    true_set = set(true)
    score = 0.0
    num_hits = 0
    for i, skill in enumerate(recommended, 1):
        if skill in true_set:
            num_hits += 1
            score += num_hits / i
    return score / len(true) if true else 0

# Evaluate on test set
print("Evaluating model...")
precisions, recalls, f1s, aps = [], [], [], []
for _, row in test_df.iterrows():
    job_title = row["core_position"]
    true_skills = row["core_skills"]
    recommended_skills = recommend_skills(job_title, top_n=10)
    
    p, r, f = precision_recall_f1(recommended_skills, true_skills)
    ap = average_precision(recommended_skills, true_skills)
    
    precisions.append(p)
    recalls.append(r)
    f1s.append(f)
    aps.append(ap)

# Compute averages
mean_precision = np.mean(precisions)
mean_recall = np.mean(recalls)
mean_f1 = np.mean(f1s)
map_score = np.mean(aps)
print(f"Mean Precision: {mean_precision:.4f}")
print(f"Mean Recall: {mean_recall:.4f}")   
print(f"Mean F1 Score: {mean_f1:.4f}")
print(f"Mean Average Precision: {map_score:.4f}")