from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import SeekerProfile
from .forms import SeekerProfileForm


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
