import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate  # For better display in terminal

# ✅ Step 1: Load and Clean the Dataset
data_path = "data/cleaned_naukri_jobs2.csv"  # Update if needed

try:
    df = pd.read_csv(data_path)
    print("✅ Dataset Loaded Successfully!")
except FileNotFoundError:
    print(f"❌ Error: File not found at {data_path}")
    exit()

# ✅ Step 2: Handling Missing Values
df.fillna("", inplace=True)

# ✅ Step 3: Combine Job Title & Skills for Text Processing
df["Combined_Text"] = df["Title"] + " " + df["Skills"].astype(str)

# ✅ Step 4: TF-IDF Vectorization
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["Combined_Text"])

# ✅ Step 5: Function to Recommend Jobs
def recommend_jobs(query, top_n=5):
    query_vec = vectorizer.transform([query])  # Convert query into vector
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix)  # Compute similarity
    similar_jobs = cosine_sim.argsort()[0][-top_n:][::-1]  # Get top N similar jobs

    recommendations = df.iloc[similar_jobs][["Title", "Company", "Location", "Skills"]]
    
    # ✅ Save recommendations to CSV
    recommendations.to_csv("recommended_jobs.csv", index=False)

    return recommendations

# ✅ Step 6: CLI Input for Job Search
if __name__ == "__main__":
    query = input("\n🔍 Enter job title or skills (e.g., 'Python Developer Machine Learning'): ")
    recommended_jobs = recommend_jobs(query)

    # ✅ Display Results in a Clean Format
    print("\n🎯 Recommended Jobs:\n")
    print(tabulate(recommended_jobs, headers='keys', tablefmt='pretty'))
