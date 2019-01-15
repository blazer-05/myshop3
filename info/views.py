from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from info.models import News

def newslist(request):
    news_list = News.objects.filter(is_active=True)
    paginator = Paginator(news_list, 2)
    page = request.GET.get('page')
    news_list = paginator.get_page(page)
    return render(request, 'news/list.html', {'news_list': news_list})

def newsdetails(request, slug):
    context = {}
    newsdetails = get_object_or_404(News, slug=slug, is_active=True)
    newsdetails.count += 1
    newsdetails.save()
    context['newsdetails'] = newsdetails
    return render(request, 'news/details.html', context)
