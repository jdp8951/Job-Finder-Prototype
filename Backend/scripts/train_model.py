import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import joblib
import os
from fuzzywuzzy import process

# ✅ Step 1: Load and Clean the Dataset
data_path = "data/cleaned_naukri_jobs.csv"  # Update if needed

try:
    df = pd.read_csv(data_path)
    print("✅ Dataset Loaded Successfully!")
except FileNotFoundError:
    print(f"❌ Error: File not found at {data_path}")
    exit()

# ✅ Step 2: Handle Missing Values
df.fillna("", inplace=True)

# ✅ Step 3: Combine Job Title & Skills for Text Processing
df["Combined_Text"] = df["Title"] + " " + df["Skills"].astype(str)

# ✅ Step 4: TF-IDF Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Combined_Text"])

# ✅ Step 5: Apply DBSCAN Clustering
eps_value = 0.45  # Reduce to allow smaller clusters
min_samples = 4   # Reduce to allow more clusters

dbscan = DBSCAN(eps=eps_value, min_samples=min_samples, metric='cosine')
df["Cluster"] = dbscan.fit_predict(tfidf_matrix)

# ✅ Step 5.1: Assign Descriptive Cluster Labels
cluster_labels = {}

for cluster in set(df["Cluster"]):
    if cluster == -1:  # Mark noise points separately
        cluster_labels[cluster] = "Noise"
        continue
    
    # Get job titles in the current cluster
    job_titles = df[df["Cluster"] == cluster]["Title"]
    
    # Find the most common job title in this cluster
    common_title = job_titles.mode()[0] if not job_titles.mode().empty else f"Cluster {cluster}"
    
    # Assign a meaningful name
    cluster_labels[cluster] = common_title

# Map cluster numbers to descriptive names
df["Cluster_Name"] = df["Cluster"].map(cluster_labels)

# ✅ Step 6: Standardize Cluster Names using Fuzzy Matching
unique_titles = df["Cluster_Name"].unique()
title_mapping = {}

for title in unique_titles:
    best_match, score = process.extractOne(title, unique_titles)
    if score > 85:  # Merge if similarity is high
        title_mapping[title] = best_match
    else:
        title_mapping[title] = title  # Keep as-is

df["Cluster_Name"] = df["Cluster_Name"].map(title_mapping)

# ✅ Step 7: Save the Model & Data
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

joblib.dump(dbscan, "models/dbscan_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
df.to_csv("data/dbscan_clustered_jobs.csv", index=False)

print(f"\n🎯 DBSCAN Model Trained Successfully!")
print("📁 Saved model: models/dbscan_model.pkl")
print("📁 Saved vectorizer: models/tfidf_vectorizer.pkl")
print("📁 Clustered jobs saved to: data/dbscan_clustered_jobs.csv")

# ✅ Compute Silhouette Score
if len(set(df["Cluster"])) > 2:  # Only if more than one cluster exists
    score = silhouette_score(tfidf_matrix, df["Cluster"])
    print(f"📊 Silhouette Score: {score:.4f} (Higher is better)")

# ✅ Display Cluster Name Mapping
print("\n🔍 Cluster Name Mapping:")
for cluster, name in cluster_labels.items():
    print(f"🟢 Cluster {cluster}: {name}")

# ✅ Show Final Cluster Distribution
print("\n🔍 Updated Cluster Distribution with Merged Names:")
print(df["Cluster_Name"].value_counts())

# ✅ Step 8: Visualize Clusters using PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(tfidf_matrix.toarray())  # Convert sparse matrix to dense

# Add PCA results to DataFrame
df["PCA1"] = X_pca[:, 0]
df["PCA2"] = X_pca[:, 1]

# Plot clusters
plt.figure(figsize=(12, 7))
sns.scatterplot(x="PCA1", y="PCA2", hue="Cluster_Name", data=df, palette="viridis", alpha=0.7)
plt.title("Job Clusters Visualization (PCA Reduced)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="Cluster Name", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()
