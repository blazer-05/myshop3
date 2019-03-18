from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from comments.forms import CommentFormCaptcha, CommentForm
from comments.models import Comment


def create_comment(request):

    if request.method != 'POST':
        raise Http404()

    if request.user.is_authenticated:
        FormClass = CommentForm
    else:
        FormClass = CommentFormCaptcha

    form = FormClass(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data['user']
        user_name = form.cleaned_data['user_name']
        email = form.cleaned_data['email']
        text = form.cleaned_data['text']

        recepients = ['blazer-05@mail.ru']

        comment = form.save(commit=False)
        comment.user = request.user if request.user.is_authenticated else None
        comment.save()

        context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment}

        message = render_to_string('admin_comment_email.html', context, request)
        email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
        return redirect(newsdetails.pk)