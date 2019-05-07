from django import template
from django.db.models import Avg, Count, Q
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

    total_review = review.count()

    paginator = Paginator(review, 10)
    page = request.GET.get('page')
    review = paginator.get_page(page)

    if not request.user.is_authenticated:
        form = ReviewFormCaptcha(initial=form_initial)  # Форма с капчей
    else:
        form = ReviewForm(initial=form_initial)  # Форма без капчи

    contex = {
        'request': request,
        'reviews': review,
        'form': form,
        'total_review': total_review,
        'rating_info': get_rating_info(product) # Рейтинг звезд
    }

    return contex


def get_rating_info(product):
    '''Рейтинг звезд'''
    return Review.objects.filter(is_active=True, product=product).aggregate(
        avg=Avg('rating'),
        stars=Count('pk'),
        stars1=Count('pk', filter=Q(rating=Review.RATING_CHOICES.terrible)),
        stars2=Count('pk', filter=Q(rating=Review.RATING_CHOICES.badly)),
        stars3=Count('pk', filter=Q(rating=Review.RATING_CHOICES.normally)),
        stars4=Count('pk', filter=Q(rating=Review.RATING_CHOICES.good)),
        stars5=Count('pk', filter=Q(rating=Review.RATING_CHOICES.perfectly)),
    )