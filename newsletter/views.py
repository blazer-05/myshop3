from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q

from myshop3 import local_settings, settings
from .models import NewsletterUser, Newsletter, Template
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
        site = local_settings.SITES
        with open(local_settings.BASE_DIR + '/newsletter/templates/newsletter/user_email/sign_up_email.txt') as f:
            signup_message = f.read()
        messages_sub = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
        html_template = get_template('newsletter/user_email/sign_up_email.html').render()
        messages_sub.attach_alternative(html_template, 'text/html')
        messages_sub.send()

        '''Письмо админу о подписке на рассылку'''
        send_mail('Уважаемый админ сайта "{}" '.format(site),
                  'Адрес эл.почты {} был подписан на новостную рассылку!'.format(to_email), from_email, [from_email])

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
            site = local_settings.SITES
            with open(local_settings.BASE_DIR + '/newsletter/templates/newsletter/user_email/unsubscribe_email.txt') as f:
                signup_message = f.read()
            message_un = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template('newsletter/user_email/unsubscribe_email.html').render()
            message_un.attach_alternative(html_template, 'text/html')
            message_un.send()

            '''Письмо админу об отписке на рассылку'''
            send_mail('Уважаемый админ сайта "{}" '.format(site),
                      'Адрес эл.почты {} был отписан от новостной рассылки.'.format(to_email), from_email, [from_email])

        else:
            messages.warning(request, 'Your email is not in the database')

    context = {
        'form': form,
    }

    return render(request, 'newsletter/unsubscribe.html', context)


@staff_member_required(login_url='https://google.com') # этот декоратор закрывает доступ к странице всех кроме superuser
def control_newsletter(request):
    '''Рассылка'''
    templates = Template.objects.filter(is_active=True)

    form = NewsletterCreationForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == Newsletter.EMAIL_STATUS_CHOICES.Published:
            subject = newsletter.subject
            body = newsletter.body
            from_email = local_settings.DEFAULT_FROM_EMAIL
            messages.success(request, 'Your messages have been sent successfully.')
            for email in newsletter.users_email.all():
                # send_mail(subject=subject, from_email=from_email, recipient_list=[email.email], message=body, fail_silently=True)
                mail = EmailMultiAlternatives(subject, body, from_email, [email.email])
                if newsletter.file:
                    mail.attach_file(instance.file.path)
                mail.content_subtype = 'html'
                mail.send(fail_silently=True)

        else:
            messages.warning(request, 'An error has occurred, please try sending a message later.')

    context = {
        'form': form,
        'templates': templates,
    }

    return render(request, 'newsletter/control_panel/control_newsletter.html', context)


def control_newsletter_list(request):
    '''Список всех рассылок'''
    newsletters = Newsletter.objects.all().order_by('-created')

    paginator = Paginator(newsletters, 20)
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
            return redirect('newsletter:control_newsletter_detail', pk=newsletter.pk)

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
            return redirect('newsletter:control_newsletter_list')
    else:
        form = NewsletterCreationForm(instance=newsletter)

    context = {
        'form': form
    }

    return render(request, 'newsletter/control_panel/control_newsletter_delete.html', context)


def control_newsletter_search(request):
    '''Поиск по рассылкам'''
    query = request.GET.get('q')

    '''Проверяем, если запрос был (http://localhost:8001/dashboard/search/) то выводим пустой кверисет'''
    if query:
        search_newsletter = Newsletter.objects.filter(
            Q(id__icontains=query)|
            Q(subject__icontains=query)|
            Q(body__icontains=query)|
            Q(status__icontains=query)|
            Q(created__icontains=query)

        )
    else:
        search_newsletter = Newsletter.objects.none()

    count_newsletter = search_newsletter.count()

    paginator = Paginator(search_newsletter, 10)
    page = request.GET.get('page')
    search_newsletter = paginator.get_page(page)

    context = {
        'search_newsletter': search_newsletter,
        'count_newsletter': count_newsletter,
        'query': query,

    }

    return render(request, 'newsletter/control_panel/control_newsletter_search.html', context)


def control_newsletter_templates(request):
    '''Товарный шаблон для рассылки'''
    templates = Template.objects.filter(is_active=True)
    site_url = 'http://myshop3.sharelink.ru:8080'

    context = {
        'templates': templates,
        'site_url': site_url,


    }

    return render(request, 'newsletter/control_panel/control_newsletter_templates.html', context)