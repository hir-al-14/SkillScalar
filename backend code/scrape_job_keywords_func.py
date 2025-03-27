import sys
import os
import pandas as pd
from jobspy import scrape_jobs
from keyword_extractor import extract_keywords
from keywords import technical_keywords_dict, full_keywords

def scrape_and_save(job_title, job_type, location):
    # Basic validation to check for empty fields
    if not job_title or not job_type or not location:
        raise ValueError("Job title, job type, and location must be provided.")

    print(f"Scraping jobs for: {job_title}, {job_type}, Location: {location}")

    # Set up the search parameters for the scrape
    search_params = {
        "site_name": ["indeed", "linkedin", "google"],
        "location": location,
        "results_wanted": 100,
        "hours_old": 72,
        "country_indeed": 'USA',
        "job_type": job_type,
        "verbose": 0
    }

    # Construct the search term based on the job title and job type
    search_params["search_term"] = f"{job_title} {job_type}"
    search_params["google_search_term"] = f"{job_title} {job_type}"

    # Scrape jobs based on the search parameters
    try:
        jobs = scrape_jobs(**search_params)
        if not jobs:
            print(f"No jobs found for {job_title} in {location}.")
            return None
    except Exception as e:
        print(f"Error occurred while scraping jobs: {e}")
        return None

    # Convert the jobs data into a pandas DataFrame
    df = pd.DataFrame(jobs)

    # Extract technical keywords for the specific job title
    role_keywords = technical_keywords_dict.get(job_title, full_keywords)
    df['technical_keywords'] = df['description'].apply(lambda x: extract_keywords(x, role_keywords))

    # Define the output CSV file name and path
    csv_file = f"{job_title.replace(' ', '_').lower()}_job_keywords.csv"
    
    try:
        # Save the DataFrame to CSV
        df.to_csv(csv_file, index=False)
        print(f"Job data saved to {csv_file}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return None

    return csv_file

if __name__ == "__main__":
    # Ensure that arguments are passed correctly
    if len(sys.argv) < 4:
        print("Usage: python scrape_job_keyword_func.py <job_title> <job_type> <location>")
        sys.exit(1)

    job_title = sys.argv[1]
    job_type = sys.argv[2]
    location = sys.argv[3]

    # Call the scrape_and_save function
    result = scrape_and_save(job_title, job_type, location)
    if result:
        print(f"Job data was successfully saved: {result}")
    else:
        print("No job data was saved.")