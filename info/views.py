from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from info.models import News


def newslist(request):
    ''' Вывод списка новостей '''

    '''Использование annotate (with_comments_count()) для вывода в шаблоне info/list.html количество комментариев к посту {{ list.comments_count }} без запросов к бд'''
    news_list = News.objects.filter(is_active=True).with_comments_count()
    paginator = Paginator(news_list, 2)
    page = request.GET.get('page')
    news_list = paginator.get_page(page)
    return render(request, 'news/list.html', {'news_list': news_list})


def newsdetails(request, slug):

    ''' Вывод полной новости '''
    newsdetails = get_object_or_404(News, slug=slug, is_active=True)

    '''подсчет количества просмотров новости с сохранением в бд'''
    newsdetails.count += 1
    newsdetails.save()

    '''подсчет общего количества комментариев к посту'''
    all_comment = newsdetails.comments.count()
    return render(request, 'news/details.html', {'newsdetails': newsdetails, 'all_comment': all_comment})


# def success(request):
#     return render(request, 'news/success.html')


