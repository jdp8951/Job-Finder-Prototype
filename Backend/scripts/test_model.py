import pandas as pd
import joblib
import os
from fuzzywuzzy import process

def load_model():
    """Load the trained DBSCAN model and TF-IDF vectorizer."""
    model_path = "models/dbscan_model.pkl"
    vectorizer_path = "models/tfidf_vectorizer.pkl"
    data_path = "data/dbscan_clustered_jobs.csv"
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path) or not os.path.exists(data_path):
        print("❌ Error: Required files not found! Make sure to train the model first.")
        exit()
    
    dbscan = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    clustered_jobs = pd.read_csv(data_path)
    
    return dbscan, vectorizer, clustered_jobs

def predict_cluster(job_title, skills):
    """Predict the job cluster based on job title and skills."""
    _, vectorizer, clustered_jobs = load_model()
    
    # Combine job title and skills for text processing
    input_text = job_title + " " + skills
    
    # Transform input using the same TF-IDF vectorizer
    X_input = vectorizer.transform([input_text])
    
    # Find the best match using fuzzy matching
    best_match, score = process.extractOne(job_title, clustered_jobs["Cluster_Name"].unique())
    
    if score > 85:  # Use fuzzy matched cluster if confidence is high
        return best_match
    else:
        return "Unknown Cluster"

# ✅ Test the model with sample inputs
if __name__ == "__main__":
    print("\n🔍 **Testing Job Clusters**")
    job_title = input("Enter Job Title: ")
    skills = input("Enter Skills (comma-separated): ")
    
    cluster = predict_cluster(job_title, skills)
    print(f"\n🎯 Predicted Cluster: {cluster}")
