from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from cart.models import Cart


def get_cart(request):
    if not hasattr(request, '_cached_cart'):
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.pk
        else:
            cart = Cart.objects.get(pk=cart_id)

        request._cached_cart = cart
    return request._cached_cart


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_token(request)
        request.cart = SimpleLazyObject(lambda: get_cart(request))
