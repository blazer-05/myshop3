from django.shortcuts import render


def user_profile(request):
    return render(request, 'profiles/user_profiles.html')
