from django import forms
from .models import SeekerProfile


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        fields = [
            'headline', 'skills', 'education', 'work_experience',
            'linkedin_url', 'github_url', 'portfolio_url',
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 5}),
            'work_experience': forms.Textarea(attrs={'rows': 5}),
        }
