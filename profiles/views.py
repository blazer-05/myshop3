from django.contrib import messages
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordChangeView
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from profiles.forms import EditProfileForm
from orders.models import Order
from shop.models import Product



@login_required
def user_profile(request):
    '''Вывод профиля и ip адреса пользователя'''
    context = {}
    # my_order = Order.objects.filter(user=request.user)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    context['ip'] = ip
    # context['my_order'] = my_order

    return render(request, 'profiles/user_profiles.html', context)


@login_required
def user_profile_edit(request):
    '''Редактирование профиля пользователя'''
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

    return render(request, 'profiles/edit_user_profile.html', {'form': form})


@login_required
def my_orders(request):
    '''Вывод всех заказов пользователя'''
    context = {}
    my_order = Order.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(my_order, 3)
    page = request.GET.get('page')
    my_order = paginator.get_page(page)

    context['my_order'] = my_order

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
    wish_list = Order.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(wish_list, 3)
    page = request.GET.get('page')
    wish_list = paginator.get_page(page)

    context['wish_list'] = wish_list

    return render(request, 'profiles/my_wish_list.html', context)


@login_required
def delete_my_wish_list(request, pk):
    '''Функция удаления товара в личном кабинете'''

    delete = get_object_or_404(Order, pk=pk, user=request.user)# user=request.user - передаем юзера т.е. юзер может удалить только свои комментарии и ни какие другие. в противном случае ошибка 404
    delete.delete()
    messages.success(request, 'Данный товар успешно удален!')
    return HttpResponseRedirect('/accounts/profile/my_wish_list/')# редиректим на страницу откуда был удален товар


class CustomPasswordChangeView(PasswordChangeView):
    '''Смена пароля в профиле пользователя'''
    success_url = reverse_lazy('user_profile')


password_change = login_required(CustomPasswordChangeView.as_view())
