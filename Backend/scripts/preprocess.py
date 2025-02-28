import pandas as pd

# Load the dataset
df = pd.read_csv("data/naukri_jobs2.csv")

# Drop duplicates
df.drop_duplicates(inplace=True)

# Remove any rows with missing essential values
df.dropna(subset=["Title", "Company", "Location", "Skills"], inplace=True)

# Convert experience to numerical range (0 if 'Fresher', else take first number)
df["Experience"] = df["Experience"].str.extract("(\d+)").fillna(0).astype(int)

# Convert Salary to numerical range (extract first number)
df["Salary"] = df["Salary"].str.extract("(\d+)").fillna(0).astype(int)

# Convert skills into a list format for better processing
df["Skills"] = df["Skills"].apply(lambda x: x.split(", ") if isinstance(x, str) else [])

# Save the cleaned data
df.to_csv("cleaned_naukri_jobs.csv", index=False)

print(f"✅ Data cleaned and saved! Total entries: {len(df)}")
