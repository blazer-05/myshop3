from datetime import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from comments.forms import CommentFormCaptcha, CommentForm, EditComment
from comments.models import Comment


def create_comment(request):
    '''Создание комментария'''

    '''Если запрос не POST, то выводим ошибку 404'''
    if request.method != 'POST':
        raise Http404()

    '''Если пользователь авторизован, то в FormClass присвамваем форму без капчи, иначе в FormClass присваиваем форму с капчей'''
    if request.user.is_authenticated:
        FormClass = CommentForm
    else:
        FormClass = CommentFormCaptcha

    '''Инициализация формы'''
    form = FormClass(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data['user']
        user_name = form.cleaned_data['user_name']
        email = form.cleaned_data['email']
        text = form.cleaned_data['text']

        recepients = ['blazer-05@mail.ru']

        comment = form.save(commit=False)
        '''Было comment.user = request.user при добавлении комментария анонимом сайт падал
        так как request.user для авторизированного это инстанс User,
        а для не авторизированного это инстанс AnonymousUser (это не модель бд)'''
        comment.user = request.user if request.user.is_authenticated else None  # Без этой проверки анонимный пользователь не мог добавить комментарий
        comment.save()

        context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment}

        message = render_to_string('admin_comment_email.html', context, request)
        email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
        #return redirect(comment.content_object.get_absolute_url())
        '''Если капча введена с ошибкой, то возвращаем ошибку с помощью ajax. Код в review_script.js'''
        return HttpResponse(status=201)
    else:
        return JsonResponse({field: list(errors) for field, errors in form.errors.items()}, status=400)


def edit_comment(request, pk):
    '''Функция редактирование комментария к новости'''
    comment = get_object_or_404(Comment, pk=pk, user=request.user) # user=request.user - передаем юзера т.е. юзер может редактировать только свои комментарии и ни какие другие. в противном случае ошибка 404
    comm_news = comment.content_object  # comment.news получаем комментарии связанные с новостью
    if request.method == 'POST':
        form = EditComment(request.POST or None, instance=comment)
        if form.is_valid():
            user = form.cleaned_data['user']
            text = form.cleaned_data['text']

            recepients = ['blazer-05@mail.ru']

            instance = form.save(commit=False)
            instance.user = request.user if request.user.is_authenticated else None
            instance.save()

            context = {'user': user, 'text': text, 'instance': instance, 'comment': comment}
            message = render_to_string('admin_edit_comment_email.html', context, request)
            email = EmailMessage('Комментарий №"{}" к статье "{}" был отредактирован'.format(comment.id, comment.content_object), message, 'blazer-05@mail.ru', recepients)
            email.content_subtype = 'html'
            email.send()

            messages.success(request, 'Ваш комментарий успешно отредактирован.')
            return HttpResponseRedirect(comm_news.get_absolute_url()) # редиректим на страницу откуда был отредактирован комментарий
    else:
        form = EditComment(instance=comment)

    context = {'comment': comment, 'form': form}

    return render(request, 'edit_comment.html', context)


def delete_comment(request, pk):
    '''Функция удвления комментария'''
    comment = get_object_or_404(Comment, pk=pk, user=request.user)# user=request.user - передаем юзера т.е. юзер может удалить только свои комментарии и ни какие другие. в противном случае ошибка 404
    comm_news = comment.content_object # comment.news получаем комментарии связанные с новостью

    recepients = ['blazer-05@mail.ru']
    context = {'comment': comment, 'comm_news': comm_news, 'delete_date': datetime.now()}
    message = render_to_string('admin_delete_comment_email.html', context, request)
    email = EmailMessage('Комментарий №"{}" к статье "{}" был удален'.format(comment.id, comment.content_object), message, 'blazer-05@mail.ru', recepients)
    email.content_subtype = 'html'
    email.send()

    comment.delete()
    messages.success(request, 'Ваш комментарий успешно удален.')
    return HttpResponseRedirect(comm_news.get_absolute_url())# редиректим на страницу откуда был удален комментарий


def like(request):
    '''Функция лайка'''
    pk = request.POST.get('pk')
    post = Comment.objects.get(id=pk)
    if request.user in post.user_like.all():
        post.user_like.remove(User.objects.get(id=request.user.id))
        post.like -= 1
        post.save()
        return HttpResponse(status=204)
    else:
        post.user_like.add(User.objects.get(id=request.user.id))
        post.like += 1
        post.save()
        return HttpResponse(status=201)



def dislike(request):
    '''Функция дизлайка'''
    pk = request.POST.get('pk')
    post = Comment.objects.get(id=pk)
    if request.user in post.user_dislike.all():
        post.user_dislike.remove(User.objects.get(id=request.user.id))
        post.dislike -= 1
        post.save()
        return HttpResponse(status=204)
    else:
        post.user_dislike.add(User.objects.get(id=request.user.id))
        post.dislike += 1
        post.save()
        return HttpResponse(status=201)

