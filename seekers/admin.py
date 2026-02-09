from django.contrib import admin
from .models import SeekerProfile


@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['headline', 'user', 'created_at']
    search_fields = ['headline', 'user__username', 'skills']
