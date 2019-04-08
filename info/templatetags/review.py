from django import template


register = template.Library()


@register.inclusion_tag('review/review.html')
def review_list(request):
    '''Создаем темплейттег'''

    return {'request': request}
