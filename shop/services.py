from shop.models import Product, Category, Attribute


def get_product_pks_from_cookie(request):
    return list(filter(bool, request.COOKIES.get('compare', '').split(':')))


def get_categories_by_cookie(request):
    product_pks = get_product_pks_from_cookie(request)
    return Category.objects.filter(product__in=product_pks).distinct


def get_products_by_cookie(request, category_slug):
    product_pks = get_product_pks_from_cookie(request)
    products = Product.objects.filter(pk__in=product_pks)
    if category_slug:
        products = products.filter(category__slug=category_slug)

    if products.values('category').distinct().count() > 1:
        return products.none()

    return products


def serialize_products(products):
    res = []
    for product in products.with_rating().prefetch_related('entry_set'):
        data = {
            'title': product.title,
            'price': product.price,
            'image_url': product.images and product.images.url,
            'rating': product.rating,
            'attributes': {
                key: value for key, value in product.entry_set.values_list('attribute', 'value__value')
            }
        }
        res.append(data)
    return res


def get_attributes(products):
    return Attribute.objects.filter(
        entry__product__in=products
    ).distinct()
