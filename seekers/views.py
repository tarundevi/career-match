from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import SeekerProfile, Application
from .forms import SeekerProfileForm, JobSearchForm, ApplicationForm
from recruiters.models import JobPosting


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

    if form.is_valid():
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
