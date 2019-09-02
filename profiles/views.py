from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordChangeView
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods

from newsletter.models import NewsletterUser
from profiles.forms import EditProfileForm
from orders.models import Order
from profiles.models import Profile
from shop.models import Product


@login_required
def user_profile(request):
    '''Вывод профиля и ip адреса пользователя'''

    context = {}

    '''Получаем объекты модели Order и сумируем их для вывода в шаблоне общего количества ордеров'''
    my_order = Order.objects.filter(user=request.user).order_by('-date')
    my_order_count = my_order.count()

    '''Получаем объекты вишлиста и сумируем их для вывода в шаблоне общего количества товаров в вишлисте'''
    wish_list = request.user.profile.products.all()
    prod_count = wish_list.count()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context['ip'] = ip
    context['prod_count'] = prod_count
    context['my_order_count'] = my_order_count

    '''Относится к подписке на рассылку новостей из личного кабинета (шаблон - user_profiles.html
    блок html кода id="menu1" - проверка по переменной{% if subscribe == True %}). Для переключателя'''
    context['subscribe'] = NewsletterUser.objects.filter(email=request.user.email).exists()

    return render(request, 'profiles/user_profiles.html', context)


@login_required
def user_profile_edit(request):
    '''Редактирование профиля пользователя'''

    title = 'Редактирование профиля'

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        '''если instance=request.user то будет сохранять в модель юзера, 
        поэтому указываем profile для сохранения в модель профиля'''
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect('/accounts/profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfileForm(instance=request.user.profile)

    return render(request, 'profiles/edit_user_profile.html', {'form': form, 'title': title})


@login_required
def my_orders(request):
    '''Вывод всех заказов пользователя'''

    context = {}

    my_order = Order.objects.filter(user=request.user).order_by('-date')
    my_order_count = my_order.count()

    title = 'Мои ордера'
    paginator = Paginator(my_order, 15)
    page = request.GET.get('page')
    my_order = paginator.get_page(page)

    context['title'] = title
    context['my_order'] = my_order
    context['my_order_count'] = my_order_count

    return render(request, 'profiles/my_orders.html', context)


@login_required
def delete_my_orders(request, pk):
    '''Функция удаления товара в личном кабинете'''

    delete = get_object_or_404(Order, pk=pk, user=request.user)# user=request.user - передаем юзера т.е. юзер может удалить только свои комментарии и ни какие другие. в противном случае ошибка 404
    delete.delete()
    messages.success(request, 'Данный товар успешно удален!')
    return HttpResponseRedirect('/accounts/profile/my-orders/')# редиректим на страницу откуда был удален товар


@login_required
def my_wish_list(request):
    '''Список избранных товаров'''

    context = {}

    wish_list = request.user.profile.products.all()
    prod_count = wish_list.count()
    title = 'Мой лист желаний'

    paginator = Paginator(wish_list, 15)
    page = request.GET.get('page')
    wish_list = paginator.get_page(page)

    context['wish_list'] = wish_list
    context['prod_count'] = prod_count
    context['title'] = title

    return render(request, 'profiles/my_wish_list.html', context)


@require_http_methods(['POST'])
def my_wish_list_add(request, pk):
    '''Сохранение товара в вишлист (избранное) с главной и др.страниц'''
    if not request.user.is_authenticated:
        raise PermissionDenied()

    product = get_object_or_404(Product, pk=pk)
    wish_list = request.user.profile.products
    if wish_list.filter(pk=pk).exists():
        wish_list.remove(product)
        return HttpResponse(status=204)
    else:
        wish_list.add(product)
        return HttpResponse(status=201)


@login_required
def delete_my_wish_list(request, pk):
    '''Функция удаления товара в личном кабинете'''

    '''Получаем профиль пользователя по products из модели Profile и удаляем по id ссылку на товар
    из промежуточной таблицы mtm products'''
    request.user.profile.products.remove(pk)
    messages.success(request, 'Данный товар успешно удален из вашего списка избранного!')
    return HttpResponseRedirect('/accounts/profile/my_wish_list/')# редиректим на страницу откуда был удален товар


class CustomPasswordChangeView(PasswordChangeView):
    '''Смена пароля в профиле пользователя'''
    success_url = reverse_lazy('user_profile')


password_change = login_required(CustomPasswordChangeView.as_view())


@login_required
def subscribe(request):
    '''Подписка на рассылку новостей из личного кабинета (шаблон - user_profiles.html)'''
    if request.method == 'POST':
        need_to_subscribe = request.POST.get('need_to_subscribe')
        if need_to_subscribe:
            NewsletterUser.objects.get_or_create(email=request.user.email)
        else:
            NewsletterUser.objects.filter(email=request.user.email).delete()

    return HttpResponse(status=200)