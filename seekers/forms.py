from django import forms
from .models import SeekerProfile
from recruiters.models import JobPosting


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


class JobSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job title...'}),
    )
    skills = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django...'}),
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City or state...'}),
    )
    salary_min = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min salary'}),
    )
    salary_max = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max salary'}),
    )
    work_location = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + JobPosting.WORK_LOCATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    visa_sponsorship = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
