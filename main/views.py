from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from .models import STATUS_CHOICES, EmployerProfile, Job, JobSeekerProfile
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EmployerProfileForm, JobSeekerProfileForm, JobForm, JobApplicationForm, JobApplication
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist

def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'main/landing.html')

@transaction.atomic
def register_employer(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = EmployerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.email  
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect("home")
    else:
        user_form = UserRegisterForm()
        profile_form = EmployerProfileForm()
    
    return render(request, "main/employer_register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


@transaction.atomic
def register_jobseeker(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        profile_form = JobSeekerProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.username  # ensure username = email
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect("home")
    else:
        user_form = UserRegisterForm()
        profile_form = JobSeekerProfileForm()
    
    return render(request, "main/seeker_register.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

def login_employer(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect("employer_login")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if hasattr(user, 'employerprofile'):
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "This account is not registered as an employer.")
                return redirect("employer_login")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("employer_login")

    return render(request, "main/employer_login.html")


def login_jobseeker(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid login credentials.")
            return redirect("login_jobseeker")

        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            if hasattr(user, 'jobseekerprofile'):
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "This login is for job seekers only.")
                return redirect("login_jobseeker")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login_jobseeker")
    return render(request, "main/seeker_login.html")


def logout_user(request):
    logout(request)
    return redirect("landing")


@login_required
def home(request):
    jobs = Job.objects.all()

    q=request.GET.get('q')
    
    # Get filters from GET request
    job_types = request.GET.getlist('job_type')
    work_modes = request.GET.getlist('work_mode')
    experiences = request.GET.getlist('experience')
    locations = request.GET.getlist('location')  
    salary = request.GET.get('salary')  
    sort_by = request.GET.get('sort_by')

    if q:
        q = q.strip()
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(employer__company_name__icontains=q)
        )

    # Apply sorting
    if sort_by == 'newest':
        jobs = jobs.order_by('-posted_on')  
    elif sort_by == 'salary_high':
        jobs = jobs.order_by('-salary')
    elif sort_by == 'salary_low':
        jobs = jobs.order_by('salary')

    # Apply filters
    if job_types:
        jobs = jobs.filter(job_type__in=job_types)
    if work_modes:
        jobs = jobs.filter(work_mode__in=work_modes)
    if experiences:
        jobs = jobs.filter(experience_required__in=experiences)
    if locations:
        jobs = jobs.filter(location__in=locations)
    if salary:
        try:
            salary_value = int(salary)
            jobs = jobs.filter(salary__gte=salary_value)
        except ValueError:
            pass  # if invalid, ignore

    # Pagination
    paginator = Paginator(jobs, 6)
    page = request.GET.get('page')
    jobs_paginated = paginator.get_page(page)

    # Detect user type
    user_type = 'unknown'
    profile = None
    try:
        if hasattr(request.user, 'employerprofile'):
            profile = EmployerProfile.objects.get(user=request.user)
            user_type = 'employer'
        elif hasattr(request.user, 'jobseekerprofile'):
            profile = JobSeekerProfile.objects.get(user=request.user)
            user_type = 'seeker'
    except Exception as e:
        print(f"Profile error: {e}")

    # Send context to template
    context = {
        'jobs': jobs_paginated,
        'selected_job_types': job_types,
        'selected_work_modes': work_modes,
        'selected_experiences': experiences,
        'selected_locations': locations,
        'salary': salary,
        'job_type_choices': Job.JOB_TYPE_CHOICES,
        'experience_choices': Job.EXPERIENCE_CHOICES,
        'work_mode_choices': Job.WORK_MODE_CHOICES,
        'city_choices': Job.CITY_CHOICES,
        'user_type': user_type,
        'profile': profile,
        'sort_by': sort_by,
        'jobs': jobs,
    }

    return render(request, 'main/home.html', context)


@login_required
def profile_view(request):
    user = request.user
    profile = None
    user_type = 'unknown'

    if hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        user_type = 'employer'
    elif hasattr(user, 'jobseekerprofile'):
        profile = user.jobseekerprofile
        user_type = 'seeker'

    return render(request, 'main/profile.html', {
        'profile': profile,
        'user_type': user_type
    })
    
def is_profile_complete(user):
    if hasattr(user, 'jobseekerprofile'):
        seeker = user.jobseekerprofile
        required_fields = [
            seeker.full_name,
            seeker.phone_number,
            seeker.gender,
            seeker.age,
            seeker.profession,
            seeker.address,
            seeker.resume,
            seeker.profile_picture,
        ]
        return all(required_fields)

    elif hasattr(user, 'employerprofile'):
        employer = user.employerprofile
        required_fields = [
            employer.full_name,
            employer.phone_number,
            employer.gender,
            employer.company_name,
            employer.company_logo,
            employer.address,
            employer.company_website,
            employer.company_size,
        ]
        return all(required_fields)

    return False

    
@login_required
def edit_profile(request):
    user = request.user
    
    if hasattr(user, 'employerprofile'):
        profile = user.employerprofile
        form_class = EmployerProfileForm
        user_type = 'employer'
    elif hasattr(user, 'jobseekerprofile'):
        profile = user.jobseekerprofile
        form_class = JobSeekerProfileForm
        user_type = 'seeker'
    else:
        return redirect('home')  # handle unknown profile

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = form_class(instance=profile)

    return render(request, 'main/edit_profile.html', {
        'form': form,
        'user_type': user_type
    })


@login_required
def upload_resume(request):
    profile = JobSeekerProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, 'main/upload_resume.html', {'form': form, 'user_type': 'seeker'})


@login_required
def applied_jobs(request):
    if not request.user.is_authenticated or request.user.user_type != 'seeker':
        return redirect('login')
    
    applications = JobApplication.objects.filter(applicant=request.user.seeker).select_related('job')
    
    context = {
        'applications': applications
    }
    return render(request, 'main/applied_jobs.html', context)


@login_required
def post_job(request):
    if not hasattr(request.user, 'employerprofile'):
        return redirect('home')

    if not is_profile_complete(request.user):
        messages.error(request, "Please complete your profile before posting a job.")
        return redirect('edit_profile')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('home')
    else:
        form = JobForm()

    return render(request, 'main/post_job.html', {'form': form})

def job_listings(request):
    jobs = Job.objects.all().order_by('-posted_on')
    return render(request, 'main/home.html', {'jobs': jobs})

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Ensure the user has a JobSeekerProfile
    try:
        seeker_profile = request.user.jobseekerprofile
    except ObjectDoesNotExist:
        messages.error(request, "You need to create your Job Seeker Profile first.")
        return redirect('edit_profile')  

    if not is_profile_complete(request.user):
        messages.warning(request, "Please complete your profile before proceeding.")
        return redirect('edit_profile')

    
    # Prevent duplicate applications
    if JobApplication.objects.filter(job=job, seeker=seeker_profile).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('home')  # or 'job_detail', job_id=job.id

    # Handle form submission
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = seeker_profile
            application.save()
            messages.success(request, "Application submitted successfully.")
            return redirect('applied_jobs')  
    else:
        form = JobApplicationForm()

    return render(request, 'main/apply_job.html', {
        'job': job,
        'form': form
    })

 
def applied_jobs(request):
    try:
        seeker_profile = JobSeekerProfile.objects.get(user=request.user)
    except JobSeekerProfile.DoesNotExist:
        seeker_profile = None

    applications = JobApplication.objects.filter(seeker=seeker_profile) if seeker_profile else []
    
    return render(request, 'main/applied_jobs.html', {'applications': applications})


@login_required
def posted_jobs(request):
    jobs = Job.objects.filter(employer=request.user).order_by('-posted_on')

    job_data = []
    for job in jobs:
        applications = JobApplication.objects.filter(job=job)
        job_data.append({
            'job': job,
            'applications': applications,
        })

    return render(request, 'main/posted_jobs.html', {'job_data': job_data})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    context = {
        'job': job,
        'is_employer': request.user.user_type == 'employer',
    }
    return render(request, 'main/_job_detail.html', context)


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'main/job_applicants.html', {'job': job, 'applications': applications})

@require_POST
@login_required
def update_application_status(request, application_id):
    app = get_object_or_404(JobApplication, id=application_id, job__employer=request.user)
    new_status = request.POST.get("status")
    if new_status in dict(JobApplication.STATUS_CHOICES).keys():
        app.status = new_status
        app.save()
    return redirect('job_applicants', job_id=app.job.id)


def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(STATUS_CHOICES).keys():
            application.status = new_status
            application.save()
            messages.success(request, "Application status updated successfully.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect('posted_jobs') 
