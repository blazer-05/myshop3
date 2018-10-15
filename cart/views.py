from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from shop.models import *
from cart.models import CartItem, Cart
from decimal import Decimal

# Корзинаа
def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)

# Добавление товара в корзину
def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug) # метод модели Cart
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse(
        {'cart_total': cart.items.count(),
         'cart_total_price': cart.cart_total,
         'items': cart_items_serializer(cart)
         })

# Удаление товара из корзины
def remove_from_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug) # метод модели Cart
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse(
        {'cart_total': cart.items.count(),
         'cart_total_price': cart.cart_total,
         'items': cart_items_serializer(cart)
         })

# Функция которая изменяет количество товара в корзине и умножает количество на цену товара
def change_item_qty(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    qty = request.GET.get('qty')
    item_id = request.GET.get('item_id')
    cart_item = CartItem.objects.get(id=int(item_id))
    cart_item.qty = int(qty)
    cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
    cart_item.save()
    new_cart_total = 0.00
    for item in cart.items.all():
        new_cart_total += float(item.item_total)
    cart.cart_total = new_cart_total
    cart.save()
    return JsonResponse(
        {'cart_total': cart.items.count(),
        'item_total': cart_item.item_total,
        'cart_total_price': cart.cart_total,
        'items': cart_items_serializer(cart)
         })

# Функция полуения объектов товара, вывод в выподающем списке корзины (изображения, описание, цена)
def cart_items_serializer(cart):
    return [{
        'id': item.product.id,
        'url': item.product.get_absolute_url(),
        'slug': item.product.slug,
        'title': item.product.title,
        'images': item.product.images and item.product.images.url,
        'qty': item.qty,
        'price': item.product.price,
        'item_total': item.item_total
    } for item in cart.items.all()]