from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from info.forms import ReviewForm, ReviewFormCaptcha, EditReviewForm
from info.models import News, Review


def newslist(request):
    ''' Вывод списка новостей '''

    '''Использование annotate (with_comments_count()) для вывода в шаблоне info/list.html 
    количество комментариев к посту {{ list.comments_count }} без запросов к бд'''
    title = 'Список новостей'

    #current_year = timezone.now().year # определяем текущий год
    '''в фильтр добавляем created__year=current_year - говорим отобразить посты за текущий год, если нужно за прошлый год, 
    то created__year=current_year - 1. на данный момент не используется эта выборка.'''
    news_list = News.objects.filter(is_active=True).with_comments_count()

    paginator = Paginator(news_list, 10)
    page = request.GET.get('page')
    news_list = paginator.get_page(page)

    context = {
        'news_list': news_list,
        'title': title,

    }
    return render(request, 'news/list.html', context)


def newsdetails(request, slug):

    ''' Вывод полной новости '''
    newsdetails = get_object_or_404(News, slug=slug, is_active=True)

    '''подсчет количества просмотров новости с сохранением в бд'''
    newsdetails.count += 1
    newsdetails.save()

    '''подсчет общего количества комментариев к посту'''
    all_comment = newsdetails.comments.count()

    return render(request, 'news/details.html', {'newsdetails': newsdetails, 'all_comment': all_comment})


def create_review(request):
    '''Создание отзыва'''

    '''Если запрос не POST, то выводим ошибку 404'''
    if request.method != 'POST':
        raise Http404()

    '''Если пользователь авторизован, то в FormClass присвамваем форму без капчи, иначе в FormClass присваиваем форму с капчей'''
    if request.user.is_authenticated:
        FormClass = ReviewForm
    else:
        FormClass = ReviewFormCaptcha

    '''Инициализация формы'''
    form = FormClass(request.POST or None, request.FILES or None)

    if form.is_valid():
        user_name = form.cleaned_data['user_name']
        product = form.cleaned_data['product']
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

        context = {'user_name': user_name, 'product': product, 'email': email, 'city': city,
                   'image': image, 'merits': merits, 'limitations': limitations,
                   'comment': comment, 'video': video, 'rating': rating, 'period': period, 'review': review}

        message = render_to_string('review/admin_review_email.html', context, request)
        email = EmailMessage('Поступил новый отзыв к товару "{}"'.format(review.product), message, 'blazer-05@mail.ru', recepients)
        email.content_subtype = 'html'
        email.send()
        messages.success(request, 'Ваш отзыв успешно отправлен, после проверки модератором он будет опубликован.')

        return HttpResponse(status=201)
    else:
        return JsonResponse({field: list(errors) for field, errors in form.errors.items()}, status=400)


def edit_review(request, pk):
    '''Редактирование отзыва'''
    review = get_object_or_404(Review, pk=pk, user=request.user)
    rev_prod = review.product
    if request.method == 'POST':
        form = EditReviewForm(request.POST or None, request.FILES or None, instance=review)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            product = form.cleaned_data['product']
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
            '''Было review.user = request.user при добавлении комментария анонимом сайт падал
            так как request.user для авторизированного это инстанс User,
            а для не авторизированного это инстанс AnonymousUser (это не модель бд)'''
            review.user = request.user if request.user.is_authenticated else None  # Без этой проверки анонимный пользователь не мог добавить комментарий
            review.save()

            context = {'user_name': user_name, 'product': product, 'email': email, 'city': city,
                       'image': image, 'merits': merits, 'limitations': limitations,
                       'comment': comment, 'video': video, 'rating': rating, 'period': period, 'review': review}

            message = render_to_string('review/admin_edit_review_email.html', context, request)
            email = EmailMessage('Отзыв №"{}" к статье "{}" был отредактирован'.format(review.id, review.product), message,
                                 'blazer-05@mail.ru', recepients)
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Ваш отзыв успешно отредактирован.')
            return HttpResponseRedirect(rev_prod.get_absolute_url())

    else:
        form = EditReviewForm(instance=review)

    return render(request, 'review/edit_review.html', {'form': form, 'review': review})


def delete_review(request, pk):
    '''Функция удаления отзыва'''
    review = get_object_or_404(Review, pk=pk, user=request.user)# user=request.user - передаем юзера т.е. юзер может удалить только свои комментарии и ни какие другие. в противном случае ошибка 404
    rev_prod = review.product # получаем комментарии связанные с новостью

    recepients = ['blazer-05@mail.ru']
    context = {'review': review, 'rev_prod': rev_prod, 'delete_date': datetime.now()}
    message = render_to_string('review/admin_delete_review_email.html', context, request)
    email = EmailMessage('Отзыв №"{}" к статье "{}" был удален'.format(review.id, review.product), message, 'blazer-05@mail.ru', recepients)
    email.content_subtype = 'html'
    email.send()

    review.delete()
    messages.success(request, 'Ваш отзыв успешно удален!')
    return HttpResponseRedirect(rev_prod.get_absolute_url())# редиректим на страницу откуда был удален комментарий


def like_review(request):
    '''Функция лайка'''
    pk = request.POST.get('pk')
    post = Review.objects.get(id=pk)

    '''Если юзер поставил лайк, то дизлайк поставить нельзя'''
    if request.user in post.user_dislike.all():
        return HttpResponse(status=400)

    if request.user in post.user_like.all():
        post.user_like.remove(User.objects.get(id=request.user.id))
        post.save()
        return HttpResponse(status=204)
    else:
        post.user_like.add(User.objects.get(id=request.user.id))
        post.save()
        return HttpResponse(status=201)


def dislike_review(request):
    '''Функция дизлайка'''
    pk = request.POST.get('pk')
    post = Review.objects.get(id=pk)

    '''Если юзер поставил дизлайк, то лайк поставить нельзя'''
    if request.user in post.user_like.all():
        return HttpResponse(status=400)

    if request.user in post.user_dislike.all():
        post.user_dislike.remove(User.objects.get(id=request.user.id))
        post.save()
        return HttpResponse(status=204)
    else:
        post.user_dislike.add(User.objects.get(id=request.user.id))
        post.save()
        return HttpResponse(status=201)
