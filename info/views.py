from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from comments.models import Comment
from info.models import News


def newslist(request):
    ''' Вывод списка новостей '''
    news_list = News.objects.filter(is_active=True).with_comments_count()
    paginator = Paginator(news_list, 2)
    page = request.GET.get('page')
    news_list = paginator.get_page(page)
    return render(request, 'news/list.html', {'news_list': news_list})


def newsdetails(request, slug):
    ''' Вывод полной новости и комментариев '''
    newsdetails = get_object_or_404(News, slug=slug, is_active=True)
    newsdetails.count += 1
    newsdetails.save()
    all_comment = newsdetails.comments.count()
    return render(request, 'news/details.html', {'newsdetails': newsdetails, 'all_comment': all_comment})


# def success(request):
#     return render(request, 'news/success.html')


