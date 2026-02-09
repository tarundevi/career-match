from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from recruiters.models import RecruiterProfile
from seekers.models import SeekerProfile


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
        auth_login(request, user)
        # Redirect based on user role
        if RecruiterProfile.objects.filter(user=user).exists():
            return redirect('recruiters:job_list')
        elif SeekerProfile.objects.filter(user=user).exists():
            return redirect('seekers:profile_detail')
        return redirect('home')


def signup_view(request):
    if request.method == 'GET':
        role = request.GET.get('role', 'seeker')
        form = SignUpForm(initial={'role': role})
        return render(request, 'signup.html', {'form': form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            # Create the corresponding profile
            if role == 'recruiter':
                RecruiterProfile.objects.create(user=user, company_name=user.username)
            else:
                SeekerProfile.objects.create(
                    user=user,
                    headline='New Job Seeker',
                    skills='',
                    education='',
                    work_experience='',
                )
            auth_login(request, user)
            if role == 'recruiter':
                return redirect('recruiters:job_list')
            return redirect('seekers:profile_update')
        return render(request, 'signup.html', {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('home')
