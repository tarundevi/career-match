from django.db import models
from django.contrib.auth.models import User


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
class JobPosting(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry'),
        ('mid', 'Mid'),
        ('senior', 'Senior'),
        ('executive', 'Executive'),
    ]

    WORK_LOCATION_CHOICES = [
        ('remote', 'Remote'),
        ('on_site', 'On-Site'),
        ('hybrid', 'Hybrid'),
    ]

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='job_postings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    skills = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    work_location = models.CharField(max_length=20, choices=WORK_LOCATION_CHOICES, default='on_site')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    visa_sponsorship = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.recruiter.company_name}"
