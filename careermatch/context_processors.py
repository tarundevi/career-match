def user_role(request):
    is_recruiter = False
    is_seeker = False
    if request.user.is_authenticated:
        from recruiters.models import RecruiterProfile
        from seekers.models import SeekerProfile
        is_recruiter = RecruiterProfile.objects.filter(user=request.user).exists()
        is_seeker = SeekerProfile.objects.filter(user=request.user).exists()
    return {
        'is_recruiter': is_recruiter,
        'is_seeker': is_seeker,
    }
