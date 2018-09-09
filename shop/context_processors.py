# Два контекстных процессора, которые выводят меню категории и фильтр сайта
from django.shortcuts import render, render_to_response

from shop.models import Category, Brand, Product

def menucategory(request):
    context = {}
    nodes = Category.objects.filter(is_activ=True)
    product = Product.objects.filter(is_activ=True)
    context['nodes'] = nodes
    context['product'] = product
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