from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),
    path('post-job/', views.post_job, name='post_job'),
    path("employer/register/", views.register_employer, name="employer_register"),
    path("jobseeker/register/", views.register_jobseeker, name="seeker_register"),
    path("employer/login/", views.login_employer, name="employer_login"),
    path("jobseeker/login/", views.login_jobseeker, name="seeker_login"),
    path("logout/", views.logout_user, name="logout"),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('upload_resume/', views.upload_resume, name="upload_resume"),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
    path('employer/posted-jobs/', views.posted_jobs, name='posted_jobs'),
    path('employer/job/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('application/<int:application_id>/status/', views.update_application_status, name='update_application_status'),
    path('application/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),

    #path('jobs/<int:job_id>/apply/', views.job_apply, name='job_apply'),
]