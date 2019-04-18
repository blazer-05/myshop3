from django import template
from django.core.paginator import Paginator
from info.models import Review
from info.forms import ReviewForm, ReviewFormCaptcha

register = template.Library()


@register.inclusion_tag('review/review.html')
def review_list(request, product):
    '''Создаем темплейттег'''

    '''Инициализация формы по продукту'''
    form_initial = {'product': product.pk}

    review = Review.objects.filter(is_active=True, product=product)

    paginator = Paginator(review, 2)
    page = request.GET.get('page')
    review = paginator.get_page(page)

    if not request.user.is_authenticated:
        form = ReviewFormCaptcha(initial=form_initial)  # Форма с капчей
    else:
        form = ReviewForm(initial=form_initial)  # Форма без капчи

    return {'request': request, 'reviews': review, 'form': form}



