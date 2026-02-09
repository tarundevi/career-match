from django import forms
from .models import JobPosting


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'description', 'requirements', 'location',
            'job_type', 'experience_level',
            'salary_min', 'salary_max',
            'application_deadline', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }
