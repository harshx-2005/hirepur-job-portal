from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

EXPERIENCE_LEVEL_CHOICES = (
    ('entry', 'Entry Level'),
    ('mid', 'Mid Level'),
    ('senior', 'Senior Level'),
)

COMPANY_SIZE_CHOICES=[
    ('1-10', '1-10 Employees'),
    ('11-50', '11-50 Employees'),
    ('51-200', '51-200 Employees'),
    ('201-500', '201-500 Employees'),
    ('500+', '500+ Employees'),
]


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

WORK_MODE_CHOICES = [
    ('remote', 'Remote'),
    ('hybrid', 'Hybrid'),
    ('onsite', 'On-site'),
]

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_website = models.URLField(max_length=200, blank=True, null=True)
    company_size = models.CharField(max_length=50, choices=COMPANY_SIZE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.company_name


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True)
    profession = models.CharField(max_length=100, blank=True)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVEL_CHOICES, blank=True)
    skills = models.TextField(blank=True)
    preferred_work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.full_name

JOB_TYPE_CHOICES = [
    ('full-time', 'Full-time'),
    ('part-time', 'Part-time'),
    ('contract', 'Contract'),
    ('internship', 'Internship'),
]


CITY_CHOICES = [
    ('Pune', 'Pune'),
    ('Mumbai', 'Mumbai'),
    ('Delhi', 'Delhi'),
    ('Hyderabad', 'Hyderabad'),
    ('Bangalore', 'Bangalore'),
    ('Chennai', 'Chennai'),
    ('Noida', 'Noida'),
    ('Gurgaon', 'Gurgaon'),
    ('Vizag', 'Vizag'),
    ('Remote', 'Remote'),
]

EXPERIENCE_CHOICES = [
    ('fresher', 'Fresher'),
    ('1-3', '1-3 years'),
    ('4-6', '4-6 years'),
    ('7-10', '7-10 years'),
    ('10+', '10+ years'),
]

EXPERIENCE_CHOICES_PRO = [
    ('Fresher', 'Fresher'),
    ('1 Year', '1 Year'),
    ('2 Years', '2 Years'),
    ('3 Years', '3 Years'),
    ('4 Years', '4 Years'),
    ('5 Years', '5 Years'),
    ('5+ Years', '5+ Years'),
]

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'Onsite'),
    ]

    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('1-3', '1 to 3 Years'),
        ('4-6', '4 to 6 Years'),
        ('7-10', '7 to 10 Years'),
        ('10+', '10+ Years'),
    ]

    CITY_CHOICES = [
        ('pune', 'Pune'),
        ('mumbai', 'Mumbai'),
        ('delhi', 'Delhi'),
        ('hyderabad', 'Hyderabad'),
        ('bangalore', 'Bangalore'),
        ('chennai', 'Chennai'),
        ('noida', 'Noida'),
        ('gurgaon', 'Gurgaon'),
        ('vizag', 'Vizag'),
        ('remote', 'Remote'),
    ]
    
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, choices=CITY_CHOICES)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES)
    salary = models.PositiveIntegerField()
    experience_required = models.CharField(max_length=100, choices=EXPERIENCE_CHOICES)
    posted_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applications/resumes/')
    cover_letter = models.FileField(upload_to='applications/cover_letters/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.seeker.full_name} - {self.job.title}"
