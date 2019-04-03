from django import template
from info.models import Review
from shop.models import Product

register=template.Library()


@register.inclusion_tag('review/review.html')
def review_list(request):
    '''Создаем темплейттег'''
    reviews = Review.objects.filter(is_active=True)
    return {'request': request, 'reviews': reviews}
