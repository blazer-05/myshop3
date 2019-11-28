# Два контекстных процессора, которые выводят меню категории и фильтр сайта
from django.db.models import Count, Q
from django.urls import reverse

from shop.models import Category, Brand, Product, Bestseller, SaleCategory, SaleProduct, PriceList
from contacts.models import Address
from easy_thumbnails.files import get_thumbnailer


def get_menu_categories():
    tmp = {}
    categories = list(Category.objects.filter(
        is_active=True
    ).annotate(
        product_items_count=Count('product', filter=Q(is_active=True)),
        subcategory_items_count=Count('children', filter=Q(is_active=True)),
    ))
    for category in categories:
        if category.level == 0:
            url = reverse('shop:catlinks', args=(category.slug,))
        elif category.level == 1:
            url = reverse('shop:catlist', args=(category.slug,))
        else:
            url = reverse('shop:shop-list', args=(category.slug,))

        tmp[category.id] = {
            'id': category.id,
            'url': url,
            'name': category.name,
            'product_items_count': category.product_items_count,
            'subcategory_items_count': category.subcategory_items_count,
            'img': category.img and category.img.url,
            'children': None
        }

        if category.parent_id:
            if not tmp[category.parent_id]['children']:
                tmp[category.parent_id]['children'] = []
            tmp[category.parent_id]['children'].append(
                tmp[category.id]
            )
            tmp[category.parent_id]['product_items_count'] += tmp[category.id]['product_items_count']
        else:
            yield tmp[category.id]


def menucategory(request):
    '''Вывод главного блока меню на всех страницах.'''
    context = {}
    product = Product.objects.filter(is_active=True)
    menu_categories = list(get_menu_categories())
    context['nodes'] = menu_categories
    context['nodes_main'] = menu_categories[:5]
    context['nodes_second'] = menu_categories[5:]
    context['product'] = product
    return context


def filters(request):
    '''Вывод фильтра в шаблон filters.html'''
    context = {}
    filters = Product.objects.all()
    context['filters'] = filters
    return context


def bestseller(request):
    '''Вывод блока bestseller в шаблон bestseller.html'''
    # context = {}
    # product_one = Product.objects.filter(is_active=True).order_by('?')[:4]
    # product_two = Product.objects.filter(is_active=True).order_by('?')[:4]
    # context['product_one'] = product_one
    # context['product_two'] = product_two
    return {'bestseller_categories': Bestseller.get_bestseller_category()} # Из модели shop/Bestseller, выводим в контекст метод get_bestseller_category()


def sale(request):
    context = {}
    context['sale_categories'] = SaleCategory.get_sale_category(request.user) # Из модели shop/SaleCategory выводим в контекст метод get_sale_category()
    context['sale_product'] = SaleProduct.get_sale_product(request.user) # Из модели shop/SaleProduct выводим в контекст метод get_sale_product()
    #context['sale_product_all'] = SaleProduct.get_sale_product_all() # Из модели shop/SaleProduct выводим в контекст метод get_sale_product_all()
    return context


def brendlogo(request):
    '''Вывод брендов в шаблоне base.html'''
    brends = Brand.objects.filter(is_active=True)
    return {'brends': brends}


def footer(request):
    '''Вывод в футер сайта адреса в шаблоне footer.html'''
    address = Address.objects.filter(is_active=True)
    return {'address': address}


def price_list(request):
    '''Прайс лист'''

    '''Если нужно вывести один прайс лист то используем кверисет с .first()
    если все, то без .first()'''
    #price = PriceList.objects.filter(is_active=True).first()
    price = PriceList.objects.filter(is_active=True)
    return {'price_list': price}