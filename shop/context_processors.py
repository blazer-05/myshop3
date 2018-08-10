# Два контекстных процессора, которые выводят меню категории и фильтр сайта
from shop.models import Category, Brand, Product

def menucategory(request): # Вывод меню в шаблон menu-category.html
    context = {}
    categories = Category.objects.filter(is_activ=True)
    products = Product.objects.filter(is_activ=True)
    brands = Brand.objects.all()
    context['categories'] = categories
    context['products'] = products
    context['brands'] = brands
    return locals()

def filters(request): # Вывод фильтра в шаблон filters.html
    context = {}
    filters = Product.objects.all()
    context['filters'] = filters
    return locals()

def bestseller(request): # Вывод фильтра в шаблон filters.html
    context = {}
    bestsellers = Brand.objects.all()
    context['bestsellers'] = bestsellers
    return locals()