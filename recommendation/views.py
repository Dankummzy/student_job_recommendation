# recommendation/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from .models import UserProfile, Job, Recommendation
from .utils import hybrid_recommendations, parse_job_description

def index(request):
    return render(request, 'recommendation/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'recommendation/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'recommendation/login.html', {'error': 'Invalid credentials'})
    return render(request, 'recommendation/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.skills = request.POST['skills']
        profile.location = request.POST['location']
        profile.preferred_roles = request.POST['preferred_roles']
        profile.save()
        return redirect('user_profile')
    return render(request, 'recommendation/user_profile.html', {'profile': profile})

@login_required
def student_input(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        profile.skills = request.POST['skills']
        profile.location = request.POST['location']
        profile.preferred_roles = request.POST['preferred_roles']
        profile.save()
        return redirect('recommendation_page', user_id=request.user.id)
    return render(request, 'recommendation/student_input.html')

@login_required
def recommendation_page(request, user_id):
    user = request.user
    profile = user.userprofile
    jobs = Job.objects.all()

    # Update the skills based on the current profile
    student_skills = profile.skills.split(',') if profile.skills else []
    preferred_roles = profile.preferred_roles.split(',') if profile.preferred_roles else []
    location = profile.location

    # Filter jobs by location and skills
    skill_matches = []
    for job in jobs:
        if location and location.lower() not in job.joblocation_address.lower():
            continue
        if any(skill.strip().lower() in job.skills.lower() for skill in student_skills):
            skill_matches.append(job.id)  # Use the Job model's primary key (id)

    # Ensure at least one job is matched, otherwise provide a default ID or handle no matches
    if not skill_matches:
        skill_matches = [0]  # Default to an arbitrary job ID or handle no matches appropriately

    recommendations = hybrid_recommendations(user_id=user_id, job_id=skill_matches[0])

    # Fetch recommended jobs from the database
    recommended_jobs = Job.objects.filter(id__in=recommendations)

    # Parse job descriptions
    parsed_jobs = []
    for job in recommended_jobs:
        parsed_job = parse_job_description(job.jobdescription)
        parsed_job.update({
            "jobtitle": job.jobtitle,
            "company": job.company,
            "joblocation_address": job.joblocation_address,
            "skills": job.skills
        })
        parsed_jobs.append(parsed_job)

    return render(request, 'recommendation/recommendation_page.html', {
        'student': user,
        'recommendations': parsed_jobs
    })

@login_required
def recommendations_history(request):
    user = request.user
    previous_recommendations = Recommendation.objects.filter(user=user).order_by('-created_at')

    # Parse job descriptions
    parsed_recommendations = []
    for recommendation in previous_recommendations:
        job = recommendation.job
        parsed_job = parse_job_description(job.jobdescription)
        parsed_job.update({
            "jobtitle": job.jobtitle,
            "company": job.company,
            "joblocation_address": job.joblocation_address,
            "skills": job.skills,
            "created_at": recommendation.created_at
        })
        parsed_recommendations.append(parsed_job)

    return render(request, 'recommendation/recommendations_history.html', {
        'previous_recommendations': parsed_recommendations
    })