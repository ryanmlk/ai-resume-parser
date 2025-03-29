from pymongo import MongoClient
import pandas as pd
import spacy
import re
from transformers import pipeline

# Step 1: Connect to MongoDB
# Replace with your MongoDB connection details (URI, database, collection)
client = MongoClient("mongodb://localhost:27017/")  # Update with your URI
db = client["jobs_data"]                   # Update with your DB name
collection = db["jobs"]             # Update with your collection name

# Step 2: Define the fields to extract
relevant_fields = {
    "name": 1,                    # Job title
    "text": 1,                    # Job posting text
    "position.careerLevel": 1,    # Career level
    "json": 1,                    # Structured JSON data
    "html": 1,                    # Raw HTML
    "salary.value": 1,            # Salary value
    "position.department": 1,     # Department
    "orgAddress.city": 1,         # City
    "orgTags": 1,                 # Tags
    "_id": 0                     # Exclude the MongoDB _id field (optional)
}

# Step 3: Query MongoDB for a random sample of 1000 records
aggregation_pipeline = [
    {"$sample": {"size": 1000}},  # Randomly select 1000 records
    {"$project": relevant_fields}  # Include only the specified fields
]

# Execute the aggregation query and fetch results as a list
sample_records = list(collection.aggregate(aggregation_pipeline))

# Step 4: Load the sample into a pandas DataFrame
df = pd.DataFrame(sample_records)

# Print basic info about the DataFrame
print(f"Retrieved {len(df)} records")
print("DataFrame Info:")
print(df.info())
print("\nFirst few rows:")
print(df.head())

# Close the MongoDB connection
client.close()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
import pandas as pd

# Vectorize titles
vectorizer = TfidfVectorizer(max_features=100, stop_words="english")
X = vectorizer.fit_transform(df["name"])

# Cluster similar titles
clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.2, linkage="average")
labels = clustering.fit_predict(X.toarray())

# Assign cluster labels to titles
df["cluster_name"] = labels

# Map clusters to a representative title (e.g., most frequent in cluster)
cluster_to_title = df.groupby("cluster_name")["name"].agg(lambda x: x.mode()[0]).to_dict()
df["standardized_name"] = df["cluster_name"].map(cluster_to_title)

print(df[["name", "standardized_name"]].head())