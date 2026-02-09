from django.urls import path
from . import views

app_name = 'seekers'

urlpatterns = [
    path('profile/', views.profile_detail, name='profile_detail'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/edit/', views.profile_update, name='profile_update'),
]
