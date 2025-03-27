import sys
import pandas as pd
import ast
from collections import Counter
from cli_pdf_parser import parse_pdf
import numpy as np

def count_skills(skills):
    return sum(skills.values())

def compute_percentage(wanted_skills, resume_skills, total_wanted_skills):
    percentage = sum((wanted_skills.get(skill, 0) / total_wanted_skills) for skill in resume_skills)
    return round(percentage * 100, 2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No job CSV file provided")
        sys.exit(1)

    job_csv_filepath = sys.argv[1]
    df = pd.read_csv(job_csv_filepath)

    # Replace NaN values in 'technical_keywords' column with empty lists
    df["technical_keywords"] = df["technical_keywords"].apply(lambda x: [] if pd.isna(x) else ast.literal_eval(x))

    resume_skills_dict = parse_pdf("Resume-Sample-1-Software-Engineer.pdf")

    match_percentages = []
    for _, row in df.iterrows():
        job_skills = Counter(set(row["technical_keywords"]))
        total_job_skills = count_skills(job_skills)

        # Compute the match percentage, ensure no division by zero
        percentage = compute_percentage(job_skills, resume_skills_dict, total_job_skills) if total_job_skills > 0 else 0
        match_percentages.append(percentage)

    df["match_percentage"] = match_percentages

    # Replace NaN values with None before saving
    df = df.replace({np.nan: None})

    df.to_csv("job_match_results.csv", index=False)

    print("Job match percentages saved to 'job_match_results.csv'.")