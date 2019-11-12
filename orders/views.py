#from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from orders.forms import OrderForm
from orders.models import Order


def order_create(request):
    '''Создание заказа'''
    '''До else отрабатывает для не авторизованного пользователя, после else для авторизованного'''
    cart = request.cart
    if request.method == 'POST':
        form = OrderForm(request.POST or None)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            buying_type = form.cleaned_data['buying_type']
            delivery_date = form.cleaned_data['delivery_date']
            address = form.cleaned_data['address']
            comment = form.cleaned_data['comment']
            recepients = ['blazer-05@mail.ru']
            user_recepients = [email]
            cart = request.cart
            order = Order.objects.create(
                #user=request.user,
                cart=request.cart,
                total=cart.discount_price,
                full_name=full_name,
                phone=phone,
                email=email,
                address=address,
                buying_type=buying_type,
                delivery_date=delivery_date,
                comment=comment,
                user=request.user if request.user.is_authenticated else None #Если пользователь не авторизован, то может сделать заказ.

            )

            context = {
                'full_name': full_name,
                'phone': phone,
                'email': email,
                'buying_type': buying_type,
                'delivery_date': delivery_date,
                'address': address,
                'comment': comment,
                'cart': cart,
                'order': order,
                #'id': order.id,
                #'date': order.date,
            }

            '''Отправляем письмо админу'''
            message = render_to_string('orders/admin_email.html', context, request)
            #email = EmailMessage('Поступил новый заказ: №' + str(order.id) + ' ' + full_name, message, 'blazer-05@mail.ru', recepients)
            if request.user.is_authenticated:
                email = EmailMessage('Поступил новый заказ. {} от пользователя "{}" '.format(order, request.user),
                                     message, 'blazer-05@mail.ru', recepients) #'blazer-05@mail.ru' - это адрес отправителя!
            else:
                email = EmailMessage('Поступил новый заказ. {} от анонимного пользователя "{}" '.format(order, full_name),
                                     message, 'blazer-05@mail.ru', recepients) #'blazer-05@mail.ru' - это адрес отправителя!
            email.content_subtype = 'html'
            email.send()

            '''Отправляем письмо пользователю'''
            user_message = render_to_string('orders/user_order_email.html', context, request)
            if request.user.is_authenticated:
                user_email = EmailMessage('Спасибо за Ваш заказ. {}'.format(order), user_message, 'blazer-05@mail.ru',
                                          to=[request.user.email])
            else:
                user_email = EmailMessage('Спасибо за Ваш заказ. {}'.format(order), user_message, 'blazer-05@mail.ru',
                                          user_recepients)
            user_email.content_subtype = 'html'
            user_email.send()

            request.cart.clear()

            return HttpResponseRedirect('thanks')
    else:
        '''Если пользователь авторизован, то инициализируем-заполняем форму значениями из профиля пользователя,
        чтобы в админке в заказе было указано от кого поступил заказ.'''
        initial = {}
        user = request.user
        if user.is_authenticated:
            profile = user.profile
            initial['full_name'] = '{} {}'.format(profile.last_name, profile.first_name)
            initial['phone'] = profile.phone
            initial['email'] = user.email

        form = OrderForm(initial=initial)

    return render(request, 'orders/orders.html', {'form': form, 'cart': cart})

