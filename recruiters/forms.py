from django import forms
from .models import JobPosting


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'description', 'requirements', 'skills',
            'location', 'job_type', 'work_location', 'experience_level',
            'salary_min', 'salary_max', 'visa_sponsorship',
            'application_deadline', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }
