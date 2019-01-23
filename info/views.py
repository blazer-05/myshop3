from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from info.models import News, Comments
from info.forms import CommentsForm


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
    comment = Comments.objects.filter(news=newsdetails) # Получаем комментарии и связываем их с новостями(news - переменная из модели Comments)

    if request.method == 'POST':
        form = CommentsForm(request.POST or None)
        if form.is_valid():
            # user = form.cleaned_data['user']
            # email = form.cleaned_data['email']
            # text = form.cleaned_data['text']
            # recepients = ['blazer-05@mail.ru']

            form = form.save(commit=False)
            if request.user == True:
                form.user = request.user
            form.news = newsdetails
            form.save()

            # base = Comments.objects.create(user=request.user, email=email, text=text)
            #
            # context = {'user': user, 'email': email, 'text': text, 'base': base}
            #
            # message = render_to_string('news/admin_comment_email.html', context, request)
            # email = EmailMessage('Поступил новый комментарий', message, 'blazer-05@mail.ru', recepients)
            # email.content_subtype = 'html'
            # email.send()
            return redirect(newsdetails, slug)
    else:
        form = CommentsForm()

    return render(request, 'news/details.html', {'newsdetails': newsdetails, 'comment': comment, 'form': form})