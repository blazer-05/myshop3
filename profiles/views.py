from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from profiles.forms import EditProfileForm
from profiles.models import Profile


@login_required
def user_profile(request):
    '''Вывод профиля'''
    '''Вывод ip адреса пользователя'''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return render(request, 'profiles/user_profiles.html', {'ip': ip})


@login_required
def user_profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect('/accounts/profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfileForm(instance=request.user.profile)

    return render(request, 'profiles/edit_user_profile.html', {'form': form})


