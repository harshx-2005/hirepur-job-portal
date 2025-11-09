from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import EmployerProfile, JobSeekerProfile, Job, JobApplication

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']  
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name', 'full_name', 'phone_number', 'gender',
            'company_logo', 'address',
        ]


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = [
            'full_name', 'phone_number', 'age', 'gender', 'address',
            'profession', 'experience_level', 'skills',
            'profile_picture', 'resume',
        ]

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name',
            'full_name',
            'phone_number',
            'gender',
            'company_logo',
            'address',
            'company_website',
            'company_size',
        ]

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = [
            'full_name',
            'phone_number',
            'age',
            'gender',
            'address',
            'profession',
            'experience_level',
            'skills',
            'preferred_work_mode',
            'profile_picture',
            'resume',
        ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location','job_type','work_mode', 'experience_required', 'salary']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']

