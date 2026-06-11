import requests
import pandas as pd
import time

# Your Adzuna credentials — replace these with yours
APP_ID = "5df155c6"
APP_KEY = "92eebeedd79507ad8c797b8a86946f43"

def get_jobs(what, where, num_pages=5):
    """
    Fetches job listings from Adzuna API.
    what = job title to search (e.g. "data analyst")
    where = location (e.g. "united states")
    num_pages = how many pages of results to get (20 jobs per page)
    """
    all_jobs = []

    for page in range(1, num_pages + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"

        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "what": what,
            "where": where,
            "results_per_page": 20,
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)

        # Check if the request worked
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("results", [])
            all_jobs.extend(jobs)
            print(f"Page {page}: got {len(jobs)} jobs")
        else:
            print(f"Error on page {page}: {response.status_code}")

        # Wait 1 second between requests so we don't overwhelm the API
        time.sleep(1)

    return all_jobs

def save_jobs(jobs, filename):
    """Takes a list of jobs and saves them as a CSV file."""
    rows = []
    for job in jobs:
        rows.append({
            "title": job.get("title", ""),
            "company": job.get("company", {}).get("display_name", ""),
            "location": job.get("location", {}).get("display_name", ""),
            "salary_min": job.get("salary_min", None),
            "salary_max": job.get("salary_max", None),
            "description": job.get("description", ""),
            "created": job.get("created", ""),
            "category": job.get("category", {}).get("label", ""),
        })

    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    print(f"Saved {len(df)} jobs to {filename}")
    return df

if __name__ == "__main__":
    # Search for these 3 job types
    searches = ["data analyst", "data engineer", "machine learning"]

    all_jobs = []
    for search in searches:
        print(f"\nSearching for: {search}")
        jobs = get_jobs(what=search, where="united states", num_pages=5)
        all_jobs.extend(jobs)

    df = save_jobs(all_jobs, "data/raw_jobs.csv")
    print(f"\nDone! Total jobs collected: {len(df)}")