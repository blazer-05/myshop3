from easy_thumbnails.alias import aliases
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from cart.models import Cart, CartProduct
from shop.models import Product


class CartProductInfoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    url = serializers.ReadOnlyField(source='product.get_absolute_url')
    slug = serializers.ReadOnlyField(source='product.slug')
    title = serializers.ReadOnlyField(source='product.title')
    images = serializers.ReadOnlyField(source='product.images.url')
    thumb = serializers.SerializerMethodField()
    price = serializers.ReadOnlyField(source='product.price')
    total = serializers.ReadOnlyField()

    class Meta:
        model = CartProduct
        fields = 'id', 'url', 'slug', 'title', 'images', 'quantity', 'price', 'total', 'thumb'

    def get_thumb(self, obj):
        if not obj.product.images:
            return
        thumbnail_options = aliases.get('cart')
        thumbnailer = get_thumbnailer(obj.product.images)
        return thumbnailer.get_thumbnail(thumbnail_options).url


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
