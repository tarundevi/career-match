from django.contrib import admin
from .models import SeekerProfile, Application


@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['headline', 'user', 'created_at']
    search_fields = ['headline', 'user__username', 'skills']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['seeker', 'job', 'applied_at']
    list_filter = ['applied_at']
    search_fields = ['seeker__user__username', 'job__title']
