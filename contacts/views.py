from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from contacts.models import Contacts, Maps, About, Address, Delivery
from contacts.forms import ContactForm, BackcallForm

# Подгружаем настройки из модуля local_settings.py.
from myshop3.local_settings import DEFAULT_FROM_EMAIL


def contact(request):
    '''Обработка формы обратной связи и вывод карты расположения объекта.'''
    context = {}
    map_url = Maps.objects.filter(is_active=True)
    address = Address.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            recepients = [DEFAULT_FROM_EMAIL] # емейл админа, на него придет сообщение от пользователя
            admin_recepients = ['blazer-05@ukr.net'] # второй емейл админа (дубль), на него придет сообщение от пользователя
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
            email = EmailMessage('Поступило новое сообщение с сайта №{} от "{}" ' .format(contact.id, full_name), message, DEFAULT_FROM_EMAIL, recepients, admin_recepients)
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
    if request.method == 'POST':
        form = BackcallForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            text = form.cleaned_data['text']
            recepients = [DEFAULT_FROM_EMAIL] # емейл админа, на него придет сообщение от пользователя
            backcall = form.save(commit=False)
            backcall.save()

            context = {
                'full_name': full_name,
                'phone': phone,
                'text': text,
                'backcall': backcall,
            }

            message = render_to_string('admin_backall_email.html', context, request)
            email = EmailMessage('Поступил заказ обратного звонка №{} от "{}" '.format(backcall.id, full_name), message, DEFAULT_FROM_EMAIL, recepients)
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
        else:
            messages.error(request, 'Произошла ошибка, попробуйте отправить еще раз.')
    else:
        form = BackcallForm()

    return render(request, 'modal_backcall.html', {'form': form})


def delivery(request):
    '''Доставка'''
    delivery = Delivery.objects.filter(is_active=True)
    return render(request, 'delivery.html', {'delivery': delivery})