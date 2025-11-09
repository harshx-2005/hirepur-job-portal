from django.contrib import admin
from .models import EmployerProfile, JobSeekerProfile, Job

admin.site.register(EmployerProfile)
admin.site.register(JobSeekerProfile)
admin.site.register(Job)
