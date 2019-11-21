# Два контекстных процессора, которые выводят меню категории и фильтр сайта

from shop.models import Category, Brand, Product, Bestseller, SaleCategory, SaleProduct, PriceList
from contacts.models import Address


def menucategory(request):
    '''Вывод главного блока меню на всех страницах.'''
    context = {}
    nodes = Category.objects.filter(is_active=True)
    product = Product.objects.filter(is_active=True)
    context['nodes'] = nodes
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