from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from shop.models import Category, Product, ProductAlbomImages, CategoryIndexPage


def index(request):
    context = {}
    cart = request.cart
    products = Product.objects.filter(is_active=True).order_by('?')[:10] # Рандомный вывод 10 товаров на главнй в первом блоке где все товары
    hotdeals = Product.objects.filter(akciya=True)
    slider_product = Product.objects.filter(is_active=True).order_by('?')[:50] # Рандомный вывод в слайдер товаров из всей базы.
    context['cart'] = cart
    context['products'] = products
    context['hotdeals'] = hotdeals
    context['slider_product'] = slider_product
    context['index_categories'] = CategoryIndexPage.get_index_categories() # Из модели shop/CategoryIndexPage, выводим в контекст метод get_index_categories()
    return render(request, 'shop/index.html', context)

def catlinks(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlinks.html', context )

def catalog(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'shop/catalog.html', {'categories': categories})

def catlist(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlist.html', context )

def shop(request):
    context = {}
    cart = request.cart
    products = Product.objects.filter(is_active=True)
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context['products'] = products
    context['cart'] = cart
    return render(request, 'shop/shop.html', context)

def shoplist(request, slug):
    context = {}
    cart = request.cart
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context['category'] = category
    context['products'] = products
    context['cart'] = cart
    return render(request, 'shop/shop-list.html', context)

def productdetails(request, product_slug):
    context = {}
    cart = request.cart
    product = get_object_or_404(Product, slug=product_slug)
    albom = ProductAlbomImages.objects.filter(is_active=True, product=product)
    category = product.category
    all_products = Product.objects.all().exclude(slug=product_slug).order_by('?')[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (все товары)
    products_from_this_category = Product.objects.filter(category=category).order_by('?')[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (товары из этой категории)
    hotdeals = Product.objects.filter(akciya=True, timer=True)
    #attribute_and_value = Entry.objects.filter(is_activ=True) # Атрибут и Значение, сейчас работает без вьюхи с models.py с переопределенного кверисета EntryQuerySet
    context['product'] = product
    context['albom'] = albom
    context['category'] = category
    context['all_products'] = all_products
    context['hotdeals'] = hotdeals
    context['products_from_this_category'] = products_from_this_category
    context['cart'] = cart
    #context['attribute_and_value'] = attribute_and_value
    return render(request, 'shop/product-details.html', context)

def wishlist(request):
    return render(request, 'shop/wishlist.html')

def myaccount(request):
    return render(request, 'shop/my-account.html')

def contact(request):
    return render(request, 'shop/contact.html')

def registration(request):
    return render(request, 'shop/registration-account.html')

def about(request):
    return render(request, 'shop/about.html')