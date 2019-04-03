from django import template
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType

from comments.forms import CommentForm, CommentFormCaptcha

register = template.Library()


@register.inclusion_tag('add_comments.html')
def add_comment(obj, request):
    """Создаем темплейттег"""

    '''Создание словаря для инициализации формы начальными значениями'''
    form_initial = {'content_type': ContentType.objects.get_for_model(obj), 'object_id': obj.pk}

    '''Получаем комментарии связанные с объектом'''
    comments = obj.comments.filter(is_active=True).order_by('-created')

    '''Счетаем общее количество коментариев к посту'''
    all_comment = comments.count()

    '''Пагинация комментариев'''
    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    '''Проверяем, если пользователь не авторизован то выводим форму с капчей иначе если авторизован,
     то выводим форму без капчи'''
    if not request.user.is_authenticated:
        form = CommentFormCaptcha(initial=form_initial)  # Форма с капчей
    else:
        form = CommentForm(initial=form_initial)  # Форма без капчи

    return {'comments': comments,
            'all_comment': all_comment,
            'form': form,
            'request': request,
            }



