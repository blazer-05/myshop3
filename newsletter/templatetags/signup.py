from django import template
from django.contrib import messages
from newsletter.models import NewsletterUser
from newsletter.forms import NewsletterUserSignUpForm

register = template.Library()


@register.inclusion_tag('newsletter/sign_up.html')
def newsletter_signup(request):
    '''Подписка на рассылку'''

    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, 'Your email already exists in our database')
        else:
            instance.save()
            messages.success(request, 'Your email has been submitted to the database')

    context = {
        'form': form,
    }

    return context





