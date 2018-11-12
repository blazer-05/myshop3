#from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from orders.forms import OrderForm
from orders.models import Order

# def order_create(request):
#     form = OrderForm(request.POST or None ) # принимаает пост запрос или ничего.
#     cart = request.cart
#
#     context = {
#         'form': form,
#         'cart': cart,
#     }
#     return render(request, 'orders/orders.html', context)


def order_create(request):
    cart = request.cart
    form = OrderForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        last_name = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']
        buying_type = form.cleaned_data['buying_type']
        address = form.cleaned_data['address']
        comment = form.cleaned_data['comment']
        Order.objects.create(
            user=request.user,
            cart=request.cart,
            total=cart.total,
            first_name=name,
            last_name=last_name,
            phone=phone,
            address=address,
            buying_type=buying_type,
            comment=comment
        )

        return HttpResponseRedirect('thanks')

    return render(request, 'orders/orders.html', {'form': form, 'cart': cart})



# def order_create(request):
#     cart = request.cart
#     form = OrderForm(request.POST or None)
#     if form.is_valid():
#         name = form.cleaned_data['name']
#         last_name = form.cleaned_data['last_name']
#         phone = form.cleaned_data['phone']
#         buying_type = form.cleaned_data['buying_type']
#         address = form.cleaned_data['address']
#         comment = form.cleaned_data['comment']
#         new_order = Order()
#         new_order.cart = request.cart
#         new_order.user = request.user
#         new_order.save()
#         new_order.first_name = name
#         new_order.last_name = last_name
#         new_order.phone = phone
#         new_order.buying_type = buying_type
#         new_order.address = address
#         new_order.comment = comment
#         new_order.total = cart.total
#         new_order.save()
#
#         return HttpResponseRedirect('thanks')
#
#     return render(request, 'orders/orders.html', {'form': form, 'cart': cart})


'''
def order_create(request):
    cart = request.cart
    if request.method == 'POST':
        form = OrderForm(request.POST or None)  # принимаает пост запрос или ничего.
        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            buying_type = form.cleaned_data['buying_type']
            address = form.cleaned_data['address']
            comment = form.cleaned_data['comment']
            new_order = Order()
            new_order.user = request.user
            new_order.save()

            context = {
                'form': form,
                'name': name,
                'last_name': last_name,
                'phone': phone,
                'buying_type': buying_type,
                'address': address,
                'comment': comment,

            }
            return HttpResponseRedirect('/orders/thanks/')
    else:
        form = OrderForm()
    return render(request, 'orders/orders.html', {'cart': cart, 'form': form})

'''