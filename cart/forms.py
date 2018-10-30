from django import forms
from django.core.exceptions import ValidationError

from cart.models import CartProduct
from shop.models import Product


class CartBaseProductForm(forms.ModelForm):
    product = forms.CharField()
    quantity = forms.IntegerField(required=False)

    class Meta:
        model = CartProduct
        fields = ('product', 'quantity')

    def __init__(self, *args, **kwargs):
        self.cart = kwargs.pop('cart')
        super().__init__(*args, **kwargs)

    def clean_product(self):
        product_slug = self.cleaned_data.get('product')
        product = Product.objects.filter(slug=product_slug).first()
        if product:
            return product
        raise ValidationError('Product not found!')


class CartAddProductForm(CartBaseProductForm):
    def save(self, commit=True):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity') or 1

        cart_product, created = CartProduct.objects.get_or_create(
            cart=self.cart, product=product, defaults={'quantity': quantity}
        )

        if not created:
            cart_product.quantity += quantity
            cart_product.save()


class CartChangeProductForm(CartBaseProductForm):

    def save(self, commit=True):
        product = self.cleaned_data.get('product')
        quantity = self.cleaned_data.get('quantity') or 1
        CartProduct.objects.filter(
            cart=self.cart, product=product
        ).update(quantity=quantity)


class CartRemoveProductForm(CartBaseProductForm):

    class Meta:
        model = CartProduct
        fields = ('product',)

    def save(self, commit=True):
        product = self.cleaned_data.get('product')
        CartProduct.objects.filter(cart=self.cart, product=product).delete()
