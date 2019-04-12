
from django import template
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from model_utils import Choices
from django.contrib import messages

from info.models import Review
from info.forms import ReviewForm, ReviewFormCaptcha


register = template.Library()


@register.inclusion_tag('review/review.html')
def review_list(request, product):
    '''Создаем отзыв в темплейттеге'''

    '''Второй параметр в функции product - это поле из модели Review - фильтруем отзыв к продукту
    В теге темплейттега добавляем второй параметр product {% review_list request product %}'''
    review = Review.objects.filter(is_active=True, product=product)

    paginator = Paginator(review, 3)
    page = request.GET.get('page')
    review = paginator.get_page(page)

    '''Если запрос не POST, то выводим ошибку 404'''
    # if request.method != 'POST':
    #     raise Http404()

    '''Если пользователь авторизован, то в FormClass присвамваем форму без капчи, иначе в FormClass присваиваем форму с капчей'''
    if request.user.is_authenticated:
        FormClass = ReviewForm
    else:
        FormClass = ReviewFormCaptcha

    '''Инициализация формы'''
    form = FormClass(request.POST or None)

    if form.is_valid():
        user = form.cleaned_data['user']
        user_name = form.cleaned_data['user_name']
        email = form.cleaned_data['email']
        city = form.cleaned_data['city']
        image = form.cleaned_data['image']
        merits = form.cleaned_data['merits']
        limitations = form.cleaned_data['limitations']
        comment = form.cleaned_data['comment']
        video = form.cleaned_data['video']
        rating = form.cleaned_data['rating']
        period = form.cleaned_data['period']

        recepients = ['blazer-05@mail.ru']

        review = form.save(commit=False)
        '''Было comment.user = request.user при добавлении комментария анонимом сайт падал
        так как request.user для авторизированного это инстанс User,
        а для не авторизированного это инстанс AnonymousUser (это не модель бд)'''
        review.user = request.user if request.user.is_authenticated else None  # Без этой проверки анонимный пользователь не мог добавить комментарий
        review.save()

        context = {'user': user, 'user_name': user_name, 'email': email, 'city': city,
                   'image': image, 'merits': merits, 'limitations': limitations,
                   'comment': comment, 'video': video, 'rating': rating, 'period': period}

        message = render_to_string('review/admin_review_email.html', context, request)
        email = EmailMessage('Поступил новый комментарий к статье "{}"'.format(review.user), message, 'blazer-05@mail.ru', recepients)
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Ваш коментарий успешно отправлен, после проверки модератором он будет опубликован.')
        return redirect(review.product)
    else:
        form = FormClass()

    return {'request': request, 'review': review, 'form': form}

    #     '''Если капча введена с ошибкой, то возвращаем ошибку с помощью ajax. Код в review_script.js'''
    #     return HttpResponse(status=201)
    # else:
    #     return JsonResponse({field: list(errors) for field, errors in form.errors.items()}, status=400)


