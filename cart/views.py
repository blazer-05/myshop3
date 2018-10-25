from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import CartProduct, Cart
from cart.serializers import CartInfoSerializer, CartProductSerializer


class CartViewSet(viewsets.GenericViewSet):
    queryset = Cart.objects.none()

    def list(self, request):
        context = {
            'cart': request.cart,
        }
        return render(request, 'cart/cart.html', context)

    @action(methods=['get'], serializer_class=CartInfoSerializer, detail=False)
    def info(self, request):
        serializer = self.get_serializer(instance=request.cart)
        return Response(serializer.data)

    @action(methods=['post'], serializer_class=CartProductSerializer, detail=False)
    def add(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity')
        cart_product, created = CartProduct.objects.get_or_create(
            cart=request.cart, product=product, defaults={'quantity': quantity}
        )
        if not created:
            cart_product.quantity += quantity
            cart_product.save()
        return Response(status=201)

    @action(methods=['post'], serializer_class=CartProductSerializer, detail=False)
    def change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        quantity = serializer.validated_data.get('quantity')
        CartProduct.objects.filter(
            cart=request.cart, product=product
        ).update(quantity=quantity)
        return Response(status=201)

    @action(methods=['post'], serializer_class=CartProductSerializer, detail=False)
    def remove(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        CartProduct.objects.filter(cart=request.cart, product=product).delete()
        return Response(status=204)


# Функция вывода в шаблон checkout данных заказа.
def checkout(request):
    cart = request.cart
    context = {
        'cart': cart,
    }
    return render(request, 'cart/checkout.html', context)