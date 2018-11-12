from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, FormView
from easy_thumbnails.alias import aliases
from easy_thumbnails.files import get_thumbnailer

from cart.forms import CartAddProductForm, CartChangeProductForm, CartRemoveProductForm


class CartTemplateView(TemplateView):
    template_name = 'cart/cart.html'


class CartInfoTemplateView(View):
    def get(self, request, *args, **kwargs):
        def get_thumb(field, alias=None):
            if not field:
                return

            if not alias:
                return field.url

            thumbnail_options = aliases.get(alias)
            thumbnailer = get_thumbnailer(field)
            return thumbnailer.get_thumbnail(thumbnail_options).url

        data = {
            'count': request.cart.count,
            'full_price': request.cart.full_price,
            'discount_price': request.cart.discount_price,
            'products': [
                {
                    'id': cartproduct.product.id,
                    'url': cartproduct.product.get_absolute_url(),
                    'slug': cartproduct.product.slug,
                    'title': cartproduct.product.title,
                    'images': get_thumb(cartproduct.product.images),
                    'thumb': get_thumb(cartproduct.product.images, 'cart'),
                    'quantity': cartproduct.quantity,
                    'price': cartproduct.product.price,
                    'discount_price': cartproduct.discount_price,
                    'total': cartproduct.full_price,
                } for cartproduct in request.cart.cartproduct_set.all()
            ],
        }

        return JsonResponse(data)


class CartFormViewMixin:
    success_status = 201
    error_status = 400

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'cart': self.request.cart})
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponse(status=self.success_status)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=self.error_status)


class CartAddFormView(CartFormViewMixin, FormView):
    form_class = CartAddProductForm


class CartChangeFormView(CartFormViewMixin, FormView):
    form_class = CartChangeProductForm


class CartRemoveFormView(CartFormViewMixin, FormView):
    form_class = CartRemoveProductForm
    success_status = 204


class CheckoutTemplateView(TemplateView):
    template_name = 'cart/checkout.html'
