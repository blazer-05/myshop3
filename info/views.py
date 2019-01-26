from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from info.models import News, Comment
from info.forms import CommentForm


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
    comments = Comment.objects.filter(news=newsdetails).order_by('-created') # Получаем комментарии и связываем их с новостями(news - переменная из модели Comments)
    all_comment = comments.count()

    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            user = form.cleaned_data['user']
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            text = form.cleaned_data['text']
            recepients = ['blazer-05@mail.ru']

            form = form.save(commit=False)
            form.user = request.user if request.user.is_authenticated else None
            form.news = newsdetails
            form.save()

            context = {'user': user, 'user_name': user_name, 'email': email, 'text': text, 'form': form,}

            message = render_to_string('news/admin_comment_email.html', context, request)
            email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(form.news), message, 'blazer-05@mail.ru', recepients)
            email.content_subtype = 'html'
            email.send()
            return redirect(newsdetails, slug)
    else:
        form = CommentForm()

    return render(request, 'news/details.html', {'newsdetails': newsdetails,
                                                 'comments': comments,
                                                 'all_comment': all_comment,
                                                 'form': form})

def admin_comment_email(request):
    return render(request, 'news/admin_comment_email.html')