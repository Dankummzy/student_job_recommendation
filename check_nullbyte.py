import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_job_recommendation.settings')
django.setup()

from recommendation.models import Job
import pandas as pd

# Load CSV data
df = pd.read_csv(r'C:\Users\user\Desktop\project-software\student_job_recommendation\recommendation\naukri_com-job_sample.csv')

# Populate the Job model
for _, row in df.iterrows():
    # Check if job already exists, if not, create it
    _, created = Job.objects.get_or_create(
        jobid=row['jobid'],
        defaults={
            'jobtitle': row['jobtitle'],
            'jobdescription': row['jobdescription'],
            'skills': row['skills'],
            'company': row['company'],
            'joblocation_address': row['joblocation_address'],
            'industry': row['industry'],
            'experience': row['experience'],
            'education': row['education'],
            'payrate': row['payrate'],
        }
    )
    if created:
        print(f"Created job: {row['jobid']} - {row['jobtitle']}")
    else:
        print(f"Job already exists: {row['jobid']}")

print("Job data loading complete!")


