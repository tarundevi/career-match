from django.db import models
from django.contrib.auth.models import User


class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    headline = models.CharField(max_length=255)
    skills = models.TextField(help_text='Comma-separated list of skills')
    education = models.TextField()
    work_experience = models.TextField()
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.headline} ({self.user.username})"
