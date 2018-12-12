# Два контекстных процессора, которые выводят меню категории и фильтр сайта
from django.shortcuts import render, render_to_response

from shop.models import Category, Brand, Product, Bestseller

def menucategory(request):
    context = {}
    nodes = Category.objects.filter(is_active=True)
    product = Product.objects.filter(is_active=True)
    context['nodes'] = nodes
    context['product'] = product
    return locals()

def filters(request): # Вывод фильтра в шаблон filters.html
    context = {}
    filters = Product.objects.all()
    context['filters'] = filters
    return locals()

def bestseller(request): # Вывод блока bestseller в шаблон bestseller.html
    context = {}
    product_one = Product.objects.filter(is_active=True).order_by('?')[:4]
    product_two = Product.objects.filter(is_active=True).order_by('?')[:4]
    context['product_one'] = product_one
    context['product_two'] = product_two
    context['bestseller_categories'] = Bestseller.get_bestseller_category()
    return locals()

def brendlogo(request): # Вывод брендов в шаблоне base.html
    brends = Brand.objects.filter(is_active=True)
    return locals()

# def base(request):
#     baseproduct = Product.objects.get(id=1)
#     return locals()