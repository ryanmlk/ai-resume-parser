import requests
import pandas as pd
from pymongo import MongoClient
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
import pickle

# LM Studio API endpoint for embeddings
API_URL = "http://127.0.0.1:1234/v1/embeddings"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["jobs_data"]
collection = db["jobs"]

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

# Fetch data from MongoDB
data = list(collection.find(
    {"core_position": {"$exists": True}, "core_skills": {"$exists": True, "$ne": []}},
    {"core_position": 1, "core_skills": 1, "_id": 1}
))
df = pd.DataFrame(data)

# Split into train and test sets
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
# model = SentenceTransformer("all-MiniLM-L6-v2")

# Training KNN model on the training set
print("Generating embeddings for training data...")
X_train = np.stack(train_df["core_position"].apply(get_embedding))
skill_lists_train = train_df["core_skills"].tolist()

# Save embeddings to file
with open('src/feedback_component/title_embeddings.pkl', 'wb') as f:
    pickle.dump(X_train, f)
print("Embeddings saved to title_embeddings.pkl")

# To load these embeddings in the future:
# with open('title_embeddings.pkl', 'rb') as f:
#     X_train = pickle.load(f)

# Train the model
print("Training KNN model...")
knn = NearestNeighbors(n_neighbors=10, metric="cosine").fit(X_train)

# Save model using pickle
with open('src/feedback_component/skill_predictor.pkl', 'wb') as f:
    pickle.dump(knn, f)