import numpy as np
import joblib
# from sklearn.externals import joblib
# import matplotlib.pyplot as plt
import os
from django.conf import settings
from .models import Job
import re


# Load pre-trained models using memory-mapping
cosine_sim_path = r'C:\Users\user\Desktop\project-software\student_job_recommendation\recommendation\cosine_similarity_matrix.joblib'
svd_matrix_collab_path = r'C:\Users\user\Desktop\project-software\student_job_recommendation\recommendation\reduced_user_job_matrix.joblib'

cosine_sim = joblib.load(cosine_sim_path, mmap_mode='r')
svd_matrix_collab = joblib.load(svd_matrix_collab_path, mmap_mode='r')

def hybrid_recommendations(user_id, job_id, top_n=5, content_weight=0.5, collab_weight=0.5):
    # Content-Based Recommendations
    content_similarities = cosine_sim[job_id]
    content_recommendations = content_similarities.argsort()[-top_n - 1:-1][::-1]

    # Collaborative Filtering Recommendations
    reconstructed_matrix = svd_matrix_collab
    collab_recommendations = np.argsort(reconstructed_matrix[user_id])[-top_n:][::-1]

    # Combine Results with Weights
    combined_scores = {}
    for idx in content_recommendations:
        combined_scores[idx] = combined_scores.get(idx, 0) + content_similarities[idx] * content_weight
    for idx in collab_recommendations:
        combined_scores[idx] = combined_scores.get(idx, 0) + reconstructed_matrix[user_id][idx] * collab_weight

    # Sort by combined scores
    combined_recommendations = sorted(combined_scores, key=combined_scores.get, reverse=True)[:top_n]

    # Return job indices (these will map to Django Job IDs)
    return combined_recommendations


# def generate_visualizations(metrics):
#     output_dir = os.path.join(settings.BASE_DIR, 'recommendation/static/visualizations/')
#     os.makedirs(output_dir, exist_ok=True)

#     # Bar Chart for Performance Metrics
#     plt.figure(figsize=(10, 5))
#     plt.bar(metrics.keys(), metrics.values(), color='skyblue')
#     plt.title('Performance Comparison')
#     plt.xlabel('Metrics')
#     plt.ylabel('Scores')
#     plt.savefig(os.path.join(output_dir, 'performance_comparison.png'))
#     plt.close()

def parse_job_description(description):
    parsed_data = {
        "job_description": "",
        "salary": "Not Disclosed by Recruiter",
        "industry": "Not specified",
        "functional_area": "Not specified",
        "role_category": "Not specified",
        "role": "Not specified",
        "keyskills": "Not specified",
        "desired_candidate_profile": "Please refer to the Job description above",
        "education": "Not specified",
        "company_profile": "Not specified",
    }

    # Define regex patterns for each part of the description
    patterns = {
        "job_description": r"Job Description\s*:\s*(.*?)\s*(Salary|Industry|Functional Area|Role Category|Role|Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "salary": r"Salary\s*:\s*(.*?)\s*(Industry|Functional Area|Role Category|Role|Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "industry": r"Industry\s*:\s*(.*?)\s*(Functional Area|Role Category|Role|Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "functional_area": r"Functional Area\s*:\s*(.*?)\s*(Role Category|Role|Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "role_category": r"Role Category\s*:\s*(.*?)\s*(Role|Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "role": r"Role\s*:\s*(.*?)\s*(Keyskills|Desired Candidate Profile|Education|Company Profile|$)",
        "keyskills": r"Keyskills\s*(.*?)\s*(Desired Candidate Profile|Education|Company Profile|$)",
        "desired_candidate_profile": r"Desired Candidate Profile\s*:\s*(.*?)\s*(Education|Company Profile|$)",
        "education": r"Education\s*[-:]\s*(.*?)\s*(Company Profile|$)",
        "company_profile": r"Company Profile\s*:\s*(.*?)\s*(Download PPT Photo 1|View Contact Details|$)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, description, re.DOTALL)
        if match:
            parsed_data[key] = match.group(1).strip()

    return parsed_data