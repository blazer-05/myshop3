from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages

from info.models import News
#from info.forms import CommentForm, CommentFormCaptcha

from django.utils.safestring import mark_safe

def newslist(request):
    ''' Вывод списка новостей '''
    news_list = News.objects.filter(is_active=True)
    paginator = Paginator(news_list, 2)
    page = request.GET.get('page')
    news_list = paginator.get_page(page)
    return render(request, 'news/list.html', {'news_list': news_list})


def newsdetails(request, slug):
    ''' Вывод полной новости и комментариев '''
    newsdetails = get_object_or_404(News, slug=slug, is_active=True)
    newsdetails.count += 1
    newsdetails.save()
    #comments = Comment.objects.filter(news=newsdetails, is_active=True).order_by('-created') # Получаем комментарии и связываем их с новостями(news - переменная из модели Comments)

    '''
    comments = newsdetails.comment.filter(is_active=True).order_by('-created') # Получаем комментарии и связываем их с новостями(news - переменная из модели Comments)

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
                #comment.news = newsdetails
                comment.object_id = newsdetails.pk
                comment.content_type = ContentType.objects.get_for_model(News)
                comment.save()

                context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment,}

                message = render_to_string('news/admin_comment_email.html', context, request)
                email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
                email.content_subtype = 'html'
                email.send()
                #messages.add_message(request, messages.INFO, 'Hello world.')
                messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
                #return HttpResponse('Hello World!!!!')
                return redirect(newsdetails, slug)
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
                # comment.news = newsdetails
                comment.object_id = newsdetails.pk
                comment.content_type = ContentType.objects.get_for_model(News)
                comment.save()

                context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'comment': comment,}

                message = render_to_string('news/admin_comment_email.html', context, request)
                email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(comment.content_object), message, 'blazer-05@mail.ru', recepients)
                email.content_subtype = 'html'
                email.send()
                #messages.add_message(request, messages.INFO, 'Hello world.')
                messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
                #return HttpResponse('Hello World!!!!')
                return redirect(newsdetails, slug)
        else:
            form = CommentForm()

'''

    return render(request, 'news/details.html', {'newsdetails': newsdetails})
'''
                                                 'comments': comments,
                                                 'all_comment': all_comment,
                                                 'form': form,
                                                 'form_user ': form_user,

                                                 })

'''

'''
def edit_comment(request, pk):
    Функция редактирование комментария к новости
    comment = get_object_or_404(Comment, pk=pk, user=request.user) # user=request.user - передаем юзера т.е. юзер может редактировать только свои комментарии и ни какие другие. в противном случае ошибка 404
    comm_news = comment.content_object  # comment.news получаем комментарии связанные с новостью
    if request.method == 'POST':
        form = CommentForm(request.POST or None, instance=comment)
        if form.is_valid():
            user = form.cleaned_data['user']
            text = form.cleaned_data['text']
            recepients = ['blazer-05@mail.ru']

            instance = form.save(commit=False)
            instance.user = request.user if request.user.is_authenticated else None
            instance.save()

            context = {'user': user, 'text': text, 'instance': instance, 'comment': comment}
            message = render_to_string('news/admin_edit_comment_email.html', context, request)
            email = EmailMessage('Комментарий №"{}" к статье "{}" был отредактирован'.format(comment.id, comment.content_object), message, 'blazer-05@mail.ru', recepients)
            email.content_subtype = 'html'
            email.send()

            messages.success(request, 'Ваш комментарий успешно отредактирован.')
            return HttpResponseRedirect(comm_news.get_absolute_url()) # редиректим на страницу откуда был отредактирован комментарий
    else:
        form = CommentForm(instance=comment)

    context = {'comment': comment, 'form': form}

    return render(request, 'news/edit_comment.html', context)


def delete_comment(request, pk):
    Функция удвления комментария
    comment = get_object_or_404(Comment, pk=pk, user=request.user)# user=request.user - передаем юзера т.е. юзер может удалить только свои комментарии и ни какие другие. в противном случае ошибка 404
    comm_news = comment.content_object # comment.news получаем комментарии связанные с новостью

    recepients = ['blazer-05@mail.ru']
    context = {'comment': comment, 'comm_news': comm_news, 'delete_date': datetime.now()}
    message = render_to_string('news/admin_delete_comment_email.html', context, request)
    email = EmailMessage('Комментарий №"{}" к статье "{}" был удален'.format(comment.id, comment.content_object), message, 'blazer-05@mail.ru', recepients)
    email.content_subtype = 'html'
    email.send()

    comment.delete()
    messages.success(request, 'Ваш комментарий успешно удален.')
    return HttpResponseRedirect(comm_news.get_absolute_url())# редиректим на страницу откуда был удален комментарий




def like(request):
    Функция лайка
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
    Функция дизлайка
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

'''


# def success(request):
#     return render(request, 'news/success.html')


# def admin_comment_email(request):
#     return render(request, 'news/admin_comment_email.html')