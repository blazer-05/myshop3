from django import template
from django.core.paginator import Paginator
from info.models import Review

register = template.Library()


@register.inclusion_tag('review/review.html')
def review_list(request, product):
    '''Создаем темплейттег'''

    '''Второй параметр в функции product - это поле из модели Review - фильтруем отзыв к продукту
    В теге темплейттега добавляем второй параметр product {% review_list request product %}'''
    review = Review.objects.filter(is_active=True, product=product)

    paginator = Paginator(review, 2)
    page = request.GET.get('page')
    review = paginator.get_page(page)

    return {'request': request, 'reviews': review}



