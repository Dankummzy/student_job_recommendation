# recommendation/models.py
from django.contrib.auth.models import User
from django.db import models

class Job(models.Model):
    jobid = models.CharField(max_length=100, unique=True)
    jobtitle = models.CharField(max_length=255)
    jobdescription = models.TextField()
    skills = models.TextField()
    company = models.CharField(max_length=255)
    joblocation_address = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=50, null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    payrate = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.jobtitle} at {self.company}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    preferred_roles = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()
    skills = models.TextField()  # Store the skills used for this recommendation
    location = models.CharField(max_length=255, null=True, blank=True)  # Store the location
    preferred_roles = models.TextField(null=True, blank=True)  # Store the preferred roles
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for recommendations

    def __str__(self):
        return f"Recommendation for {self.user.username} -> {self.job.jobtitle}"

