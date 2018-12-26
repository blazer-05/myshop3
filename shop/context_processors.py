# Два контекстных процессора, которые выводят меню категории и фильтр сайта

from shop.models import Category, Brand, Product, Bestseller, SaleCategory, SaleProduct

def menucategory(request): # Вывод главного блока меню на всех страницах.
    context = {}
    nodes = Category.objects.filter(is_active=True)
    product = Product.objects.filter(is_active=True)
    context['nodes'] = nodes
    context['product'] = product
    return context

def filters(request): # Вывод фильтра в шаблон filters.html
    context = {}
    filters = Product.objects.all()
    context['filters'] = filters
    return context

def bestseller(request): # Вывод блока bestseller в шаблон bestseller.html
    # context = {}
    # product_one = Product.objects.filter(is_active=True).order_by('?')[:4]
    # product_two = Product.objects.filter(is_active=True).order_by('?')[:4]
    # context['product_one'] = product_one
    # context['product_two'] = product_two
    return {'bestseller_categories': Bestseller.get_bestseller_category()} # Из модели shop/Bestseller, выводим в контекст метод get_bestseller_category()

def sale(request):
    context = {}
    context['sale_categories'] = SaleCategory.get_sale_category() # Из модели shop/SaleCategory выводим в контекст метод get_sale_category()
    context['sale_product'] = SaleProduct.get_sale_product() # Из модели shop/SaleProduct выводим в контекст метод get_sale_product()
    #context['sale_product_all'] = SaleProduct.get_sale_product_all() # Из модели shop/SaleProduct выводим в контекст метод get_sale_product_all()
    return context


def brendlogo(request): # Вывод брендов в шаблоне base.html
    brends = Brand.objects.filter(is_active=True)
    return {'brends': brends}
