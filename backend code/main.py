import json
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import pandas as pd
import os
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model to validate input data
class JobSearchRequest(BaseModel):
    job_title: str
    job_type: str
    location: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Job Search API!"}

@app.post("/search")
def search_jobs(request: JobSearchRequest):
    job_title = request.job_title
    job_type = request.job_type
    location = request.location

    # Define job CSV file path based on input (you could modify this logic as per your requirements)
    job_csv_filepath = f"{job_title.replace(' ', '_').lower()}_job_keywords.csv"
    
    # Run skill_comparer.py directly
    skill_comparer_script = "skill_comparer.py"
    
    # Pass the job CSV path to the skill_comparer script
    process_compare = subprocess.run(
        ["python", skill_comparer_script, job_csv_filepath],
        capture_output=True,
        text=True
    )

    if process_compare.returncode != 0:
        return {"error": "Failed to compare job skills", "details": process_compare.stderr}

    # Log if job match results CSV exists
    if os.path.exists("job_match_results.csv"):
        print("job_match_results.csv has been generated.")
    else:
        print("Error: job_match_results.csv was not generated.")

    # Load job match results (this assumes the output file from skill_comparer.py is `job_match_results.csv`)
    try:
        df = pd.read_csv("job_match_results.csv")
        df = df.replace({np.nan: None})
        job_matches = df.to_dict(orient="records")
        # Log job matches data
        print(f"Job Matches: {job_matches}")
    except Exception as e:
        return {"error": "Failed to load job match results", "details": str(e)}

    return {"message": "Job search successful", "jobs": job_matches}