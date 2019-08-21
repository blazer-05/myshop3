from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from myshop3 import local_settings
from .models import NewsletterUser, Newsletter
from .forms import NewsletterUserSignUpForm, NewsletterCreationForm


def subscribe(request):
    '''Подписка на рассылку'''
    if not request.is_ajax() or request.method != 'POST':
        return HttpResponseForbidden()

    form = NewsletterUserSignUpForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'message': 'Enter a valid email address'}, status=400)

    email = form.cleaned_data.get('email')
    if NewsletterUser.objects.filter(email=email).exists():
        message = 'Your email already exists in our database'
    else:
        form.save()
        message = 'Your email has been submitted to the database'

        subject = 'Thank You For Joining Our Newsletter'
        from_email = local_settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        with open(local_settings.BASE_DIR + '/newsletter/templates/newsletter/user_email/sign_up_email.txt') as f:
            signup_message = f.read()
        messages = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
        html_template = get_template('newsletter/user_email/sign_up_email.html').render()
        messages.attach_alternative(html_template, 'text/html')
        messages.send()

    return JsonResponse({'message': message}, status=201)


def newsletter_unsubscribe(request):
    '''Отписка от рассылки'''
    form = NewsletterUserSignUpForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, 'Your email has been removed')

            subject = 'You have unsubscribe'
            from_email = local_settings.DEFAULT_FROM_EMAIL
            to_email = [instance.email]
            with open(local_settings.BASE_DIR + '/newsletter/templates/newsletter/user_email/unsubscribe_email.txt') as f:
                signup_message = f.read()
            message_un = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template('newsletter/user_email/unsubscribe_email.html').render()
            message_un.attach_alternative(html_template, 'text/html')
            message_un.send()

        else:
            messages.warning(request, 'Your email is not in the database')

    context = {
        'form': form,
    }

    return render(request, 'newsletter/unsubscribe.html', context)


def control_newsletter(request):
    '''Рассылка'''
    form = NewsletterCreationForm(request.POST or None)

    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == 'Published':
            subject = newsletter.subject
            body = newsletter.body
            from_email = local_settings.DEFAULT_FROM_EMAIL
            for email in newsletter.email.all():
                send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body, fail_silently=True)

    context = {
        'form': form
    }

    return render(request, 'newsletter/control_panel/control_newsletter.html', context)


def control_newsletter_list(request):
    '''Список всех рассылок'''
    newsletters = Newsletter.objects.all()

    paginator = Paginator(newsletters, 2)
    page = request.GET.get('page')
    newsletters = paginator.get_page(page)

    context = {
        'newsletters': newsletters,
    }

    return render(request,'newsletter/control_panel/control_newsletter_list.html', context)


def control_newsletter_detail(request, pk):
    '''Детальный вывод рассылки'''
    newsletter = get_object_or_404(Newsletter, pk=pk)

    context = {
        'newsletter': newsletter
    }

    return render(request, 'newsletter/control_panel/control_newsletter_detail.html', context)


def control_newsletter_edit(request, pk):
    '''Редактирование рассылки'''
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save()
            if newsletter.status == 'Published':
                subject = newsletter.subject
                body = newsletter.body
                from_email = local_settings.DEFAULT_FROM_EMAIL
                for email in newsletter.email.all():
                    send_mail(subject=subject, from_email=from_email, recipient_list=[email], message=body,
                              fail_silently=True)
            return redirect('control_newsletter_detail', pk=newsletter.pk)

    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form
    }

    return render(request, 'newsletter/control_panel/control_newsletter.html', context)


def control_newsletter_delete(request, pk):
    '''Удаление рассылки'''
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter.delete()
            return redirect('control_newsletter_list')
    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form
    }

    return render(request, 'newsletter/control_panel/control_newsletter_delete.html', context)