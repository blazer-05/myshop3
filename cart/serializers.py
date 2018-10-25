from rest_framework import serializers

from cart.models import Cart, CartProduct
from shop.models import Product


class CartProductInfoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    url = serializers.ReadOnlyField(source='product.get_absolute_url')
    slug = serializers.ReadOnlyField(source='product.slug')
    title = serializers.ReadOnlyField(source='product.title')
    images = serializers.ReadOnlyField(source='product.images.url')
    price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = CartProduct
        fields = 'id', 'url', 'slug', 'title', 'images', 'quantity', 'price'


class CartInfoSerializer(serializers.ModelSerializer):
    count = serializers.ReadOnlyField()
    total = serializers.ReadOnlyField()
    products = CartProductInfoSerializer(source='cartproduct_set', many=True)

    class Meta:
        model = Cart
        fields = 'count', 'total', 'products'


class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='slug', queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=1, required=False)

    class Meta:
        model = CartProduct
        fields = 'id', 'quantity', 'product'
