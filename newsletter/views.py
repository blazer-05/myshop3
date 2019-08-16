from django.shortcuts import render
from django.contrib import messages
from .models import NewsletterUser
from .forms import NewsletterUserSignUpForm


'''Подписка на рассылку осуществляется через теплейт тег signup.py'''


def newsletter_unsubscribe(request):
    '''Отписка от рассылки'''
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been removed')
        else:
            messages.warning(request, 'Your email is not in the database')

    context = {
        'form': form,
    }

    return render(request, 'newsletter/unsubscribe.html', context)