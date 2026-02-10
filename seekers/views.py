from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SeekerProfile, Application
from .forms import SeekerProfileForm, JobSearchForm, ApplicationForm
from recruiters.models import JobPosting
from django.urls import reverse

import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from django.http import JsonResponse
import json
import math


def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2 # chcek the wiki to make sure formula is right but this is what i got
    c = 2 * math.asin(math.sqrt(a))
    
    r = 3959
    
    return c * r


def _filter_jobs(form, jobs):
    if not form.is_valid():
        return jobs
    
    title = form.cleaned_data.get('title')
    skills = form.cleaned_data.get('skills')
    location = form.cleaned_data.get('location')
    salary_min = form.cleaned_data.get('salary_min')
    salary_max = form.cleaned_data.get('salary_max')
    work_location = form.cleaned_data.get('work_location')
    visa_sponsorship = form.cleaned_data.get('visa_sponsorship')

    if title:
        jobs = jobs.filter(title__icontains=title)
    if skills:
        jobs = jobs.filter(skills__icontains=skills)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if salary_min:
        jobs = jobs.filter(salary_max__gte=salary_min)
    if salary_max:
        jobs = jobs.filter(salary_min__lte=salary_max)
    if work_location:
        jobs = jobs.filter(work_location=work_location)
    if visa_sponsorship:
        jobs = jobs.filter(visa_sponsorship=True)
    
    return jobs


@login_required
def profile_detail(request):
    profile = get_object_or_404(SeekerProfile, user=request.user)
    return render(request, 'seekers/profile_detail.html', {'profile': profile})


@login_required
def profile_create(request):
    if SeekerProfile.objects.filter(user=request.user).exists():
        return redirect('seekers:profile_detail')
    if request.method == 'POST':
        form = SeekerProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('seekers:profile_detail')
    else:
        form = SeekerProfileForm()
    return render(request, 'seekers/profile_form.html', {'form': form})


@login_required
def profile_update(request):
    profile = get_object_or_404(SeekerProfile, user=request.user)
    if request.method == 'POST':
        form = SeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('seekers:profile_detail')
    else:
        form = SeekerProfileForm(instance=profile)
    return render(request, 'seekers/profile_form.html', {'form': form, 'profile': profile})


def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    jobs = _filter_jobs(form, jobs)
    return render(request, 'seekers/job_search.html', {'form': form, 'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    return render(request, 'seekers/job_detail.html', {'job': job})


@login_required
def job_apply(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, is_active=True)
    seeker = get_object_or_404(SeekerProfile, user=request.user)

    if Application.objects.filter(seeker=seeker, job=job).exists():
        messages.info(request, 'You have already applied to this job!')
        return redirect('seekers:job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.seeker = seeker
            application.job = job
            application.save()
            messages.success(request, 'Your application has been submitted!')
            return redirect('seekers:job_detail', pk=pk)
    else:
        form = ApplicationForm()

    return render(request, 'seekers/job_apply.html', {'form': form, 'job': job})


def job_map(request):
    """Render a folium map with markers for jobs matching search filters and distance."""
    form = JobSearchForm(request.GET or None)
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    jobs = _filter_jobs(form, jobs)
    
    user_lat = request.GET.get('user_lat')
    user_lon = request.GET.get('user_lon')
    max_distance = request.GET.get('max_distance')
    
    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except (ValueError, TypeError):
            user_lat = user_lon = None
    
    if max_distance:
        try:
            max_distance = float(max_distance)
        except (ValueError, TypeError):
            max_distance = None

    if user_lat and user_lon:
        m = folium.Map(location=[user_lat, user_lon], zoom_start=10)
        folium.Marker(
            [user_lat, user_lon], 
            popup="Your Location",
            icon=folium.Icon(color='red', icon='home')
        ).add_to(m)
    else:
        m = folium.Map(location=[39.5, -98.35], zoom_start=4)

    geolocator = Nominatim(user_agent='career_match_app')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=1)

    markers_added = 0
    lat_sum = 0.0
    lon_sum = 0.0
    jobs_with_coords = []

    for job in jobs:
        if not job.location:
            continue
        try:
            loc = geocode(job.location)
        except Exception:
            loc = None

        if not loc:
            continue

        lat = loc.latitude
        lon = loc.longitude
        
        if user_lat and user_lon and max_distance:
            distance = calculate_distance(user_lat, user_lon, lat, lon)
            if distance > max_distance:
                continue

        popup_html = f"<strong>{job.title}</strong><br>{job.recruiter.company_name}<br>{job.location}<br>"
        if user_lat and user_lon:
            distance = calculate_distance(user_lat, user_lon, lat, lon)
            popup_html += f"Distance: {distance:.1f} miles<br>"
        detail_url = reverse('seekers:job_detail', args=[job.pk])
        popup_html += f"<a href=\"{detail_url}\" target=\"_top\" rel=\"noopener noreferrer\">View Details</a>"

        folium.Marker([lat, lon], popup=folium.Popup(popup_html, max_width=300)).add_to(m)

        markers_added += 1
        lat_sum += lat
        lon_sum += lon
        jobs_with_coords.append(job)

    if markers_added and not (user_lat and user_lon):
        avg_lat = lat_sum / markers_added
        avg_lon = lon_sum / markers_added
        m.location = [avg_lat, avg_lon]
        m.zoom_start = 6

    map_html = m._repr_html_()

    return render(request, 'seekers/job_map.html', {
        'map': map_html, 
        'jobs': jobs_with_coords,
        'user_lat': user_lat,
        'user_lon': user_lon,
        'max_distance': max_distance or 50  
    })
