from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import folium

from .models import JobPosting
from .forms import JobPostingForm


@login_required
def job_list(request):
    jobs = JobPosting.objects.filter(
        recruiter=request.user.recruiter_profile
    ).order_by('-created_at')
    return render(request, 'recruiters/job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, recruiter=request.user.recruiter_profile)
    map_html = None
    if job.latitude and job.longitude:
        m = folium.Map(location=[job.latitude, job.longitude], zoom_start=13)
        folium.Marker(
            [job.latitude, job.longitude],
            popup=f"<strong>{job.title}</strong><br>{job.location}",
            icon=folium.Icon(color='blue', icon='briefcase', prefix='fa'),
        ).add_to(m)
        map_html = m._repr_html_()
    return render(request, 'recruiters/job_detail.html', {'job': job, 'map': map_html})


@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user.recruiter_profile
            job.save()
            return redirect('recruiters:job_list')
    else:
        form = JobPostingForm()
    return render(request, 'recruiters/job_form.html', {'form': form})


@login_required
def job_update(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, recruiter=request.user.recruiter_profile)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('recruiters:job_list')
    else:
        form = JobPostingForm(instance=job)
    return render(request, 'recruiters/job_form.html', {'form': form, 'job': job})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobPosting, pk=pk, recruiter=request.user.recruiter_profile)
    if request.method == 'POST':
        job.delete()
        return redirect('recruiters:job_list')
    return render(request, 'recruiters/job_confirm_delete.html', {'job': job})
