# Два контекстных процессора, которые выводят меню категории и фильтр сайта
from django.shortcuts import render, render_to_response

from shop.models import Category, Brand, Product

def menucategory(request): # Вывод меню в шаблон menu-category.html
    context = {}
    nodes = Category.objects.filter(is_activ=True)
    current_category = Category.objects.get(id=1)
    #root_category_id = current_category.get_root().id
    context['nodes'] = nodes
    context['current_category'] = current_category
    #context['root_category_id'] = root_category_id
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