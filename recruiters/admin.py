from django.contrib import admin
from .models import RecruiterProfile, JobPosting


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'phone']
    search_fields = ['company_name', 'user__username']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'job_type', 'experience_level', 'is_active', 'created_at']
    list_filter = ['job_type', 'experience_level', 'is_active']
    search_fields = ['title', 'description', 'recruiter__company_name']
    date_hierarchy = 'created_at'
