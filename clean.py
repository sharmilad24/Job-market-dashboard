import pandas as pd
import re

def clean_jobs(input_file, output_file):
    # Load the raw data
    df = pd.read_csv(input_file)
    print(f"Raw data: {len(df)} rows")

    # 1. Remove duplicate rows (same job posted twice)
    df = df.drop_duplicates(subset=["title", "company", "location"])

    # 2. Clean up text columns — strip extra spaces, make consistent case
    df["title"] = df["title"].str.strip().str.title()
    df["company"] = df["company"].str.strip().str.title()
    df["location"] = df["location"].str.strip()

    # 3. Handle missing salaries — fill with the median (middle value)
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")
    df["salary_avg"] = (df["salary_min"] + df["salary_max"]) / 2
    median_salary = df["salary_avg"].median()
    df["salary_avg"] = df["salary_avg"].fillna(median_salary)

    # 4. Extract key skills from descriptions using keyword matching
    skills = ["python", "sql", "tableau", "power bi", "spark", "aws",
              "excel", "r", "machine learning", "pytorch", "tensorflow",
              "pandas", "java", "scala", "dbt", "airflow", "kafka"]

    for skill in skills:
        col_name = skill.replace(" ", "_")
        df[col_name] = df["description"].str.lower().str.contains(
            skill, na=False
        ).astype(int)

    # 5. Add a seniority label based on job title
    def get_seniority(title):
        title = str(title).lower()
        if any(w in title for w in ["senior", "sr.", "lead", "principal", "staff"]):
            return "Senior"
        elif any(w in title for w in ["junior", "jr.", "entry", "intern", "associate"]):
            return "Junior"
        else:
            return "Mid"

    df["seniority"] = df["title"].apply(get_seniority)

    # 6. Drop rows with no description (they're useless)
    df = df.dropna(subset=["description"])

    df.to_csv(output_file, index=False)
    print(f"Clean data: {len(df)} rows saved to {output_file}")
    return df

if __name__ == "__main__":
    df = clean_jobs("data/raw_jobs.csv", "data/clean_jobs.csv")