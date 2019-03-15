

from django import template
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.core.paginator import Paginator

from django.shortcuts import redirect
from django.template.loader import render_to_string

from comments.models import Comment
from comments.forms import CommentForm, CommentFormCaptcha
from info.models import News

register=template.Library()

@register.inclusion_tag('add_comments.html')
def add_comment(newsdetails, request):
    comments = Comment.objects.filter(is_active=True).order_by('-created')

    all_comment = comments.count()

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    form = CommentFormCaptcha() # Форма с капчей
    form_user = CommentForm()   # Форма без капчи

    # Если ползователь не авторизован то показываем форму с капчей
    if not request.user.is_authenticated:
        form = CommentFormCaptcha(request.POST or None)

        if request.method == 'POST':
            if form.is_valid():
                user = form.cleaned_data['user']
                user_name = form.cleaned_data['user_name']
                email = form.cleaned_data['email']
                text = form.cleaned_data['text']
                recepients = ['blazer-05@mail.ru']

                comment = form.save(commit=False)
                # parent_pk = request.POST.get('parent')
                # if parent_pk and parent_pk.isnumeric():
                #     comment.parent = Comment.objects.filter(pk=parent_pk).first()
                comment.user = request.user if request.user.is_authenticated else None
                comment.object_id = newsdetails.pk
                comment.content_type = ContentType.objects.get_for_model(newsdetails)
                comment.save()

                context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment,}

                message = render_to_string('news/admin_comment_email.html', context, request)
                email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
                email.content_subtype = 'html'
                email.send()
                messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
                return redirect(newsdetails.pk)
        else:
            form = CommentFormCaptcha()

    # Если ползователь авторизован то показываем форму без капчи
    else:
        form_user = CommentForm(request.POST or None)

        if request.method == 'POST':
            if form_user.is_valid():
                user = form_user.cleaned_data['user']
                user_name = form_user.cleaned_data['user_name']
                email = form_user.cleaned_data['email']
                text = form_user.cleaned_data['text']
                recepients = ['blazer-05@mail.ru']

                comment = form_user.save(commit=False)
                # parent_pk = request.POST.get('parent')
                # if parent_pk and parent_pk.isnumeric():
                #     comment.parent = Comment.objects.filter(pk=parent_pk).first()
                comment.user = request.user if request.user.is_authenticated else None
                comment.object_id = newsdetails.pk
                comment.content_type = ContentType.objects.get_for_model(newsdetails)
                comment.save()

                context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment}

                message = render_to_string('news/admin_comment_email.html', context, request)
                email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
                email.content_subtype = 'html'
                email.send()
                messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
                return redirect(newsdetails)
        else:
            form = CommentForm()

    return {'comments': comments,
            'all_comment': all_comment,
            'form': form,
            'form_user ': form_user,
            'request': request,
            }

