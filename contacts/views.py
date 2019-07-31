from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from contacts.models import Contacts, Maps, About
from contacts.forms import ContactForm


def contact(request):
    '''Обработка формы обратной связи и вывод карты расположения объекта.'''
    context = {}
    map_url = Maps.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            recepients = ['blazer-05@mail.ru']
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
            email = EmailMessage('Поступило новое сообщение с сайта', message, 'blazer-05@mail.ru', recepients)
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return HttpResponseRedirect('/contact/')
        else:
            messages.error(request, 'Произошла ошибка, попробуйте отправить еще раз.')
    else:
        form = ContactForm()

    context['map_url'] = map_url
    context['form'] = form

    return render(request, 'contact.html', context)


def about(request):
    return render(request, 'about.html')
