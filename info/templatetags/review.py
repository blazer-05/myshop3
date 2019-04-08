from django import template
from django.shortcuts import render

from info.models import Review
from shop.models import Product

register = template.Library()


def create_review(request):
    reviews = Review.objects.filter(is_active=True)
    return render(request, 'review/create_review.html', {'reviews': reviews})


@register.inclusion_tag('review/review.html')
def review_list(request):
    '''Создаем темплейттег'''

    return {'request': request}
