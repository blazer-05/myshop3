from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from contacts.models import Contacts, Maps, About, Address
from contacts.forms import ContactForm, BackcallForm

# Подгружаем настройки из модуля local_settings.py.
from myshop3.local_settings import DEFAULT_FROM_EMAIL


def contact(request):
    '''Обработка формы обратной связи и вывод карты расположения объекта.'''
    context = {}
    map_url = Maps.objects.filter(is_active=True)
    address = Address.objects.get(id=1)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            recepients = [DEFAULT_FROM_EMAIL]
            contact = form.save(commit=False)
            contact.save()

            context = {
                'full_name': full_name,
                'phone': phone,
                'email': email,
                'text': text,
                'contact': contact,
            }

            message = render_to_string('admin_contact_email.html', context, request)
            email = EmailMessage('Поступило новое сообщение с сайта', message, DEFAULT_FROM_EMAIL, recepients)
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return HttpResponseRedirect('/contact/')
        else:
            messages.error(request, 'Произошла ошибка, попробуйте отправить еще раз.')
    else:
        form = ContactForm()

    context['map_url'] = map_url
    context['address'] = address
    context['form'] = form

    return render(request, 'contact.html', context)


def about(request):
    '''О магазине'''
    about = About.objects.filter(is_active=True)
    context = {
        'about': about,
    }
    return render(request, 'about.html', context)


def backcall(request):
    '''Обратный звонок'''
    form = BackcallForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        full_name = form.cleaned_data['full_name']
        phone = form.cleaned_data['phone']
        text = form.cleaned_data['text']
        recepients = [DEFAULT_FROM_EMAIL]
        backcall = form.save(commit=False)
        backcall.save()

        context = {
            'full_name': full_name,
            'phone': phone,
            'text': text,
            'backall': backcall,
        }

        message = render_to_string('admin_contact_email.html', context, request)
        email = EmailMessage('Поступил заказ на обратный звонок №{} от "{}" '.format(backcall.id, full_name), message, DEFAULT_FROM_EMAIL, recepients)
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Ваше сообщение успешно отправлено!')
        form = BackcallForm()

    return render(request, 'modal_backcall.html', {'form': form})