
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render_to_response

from cart.views import *
from shop.models import Category, Brand, Product, ProductAlbomImages


def index(request):
    context = {}
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    products = Product.objects.filter(is_active=True)
    hotdeals = Product.objects.filter(akciya=True)
    slider_product = Product.objects.filter(is_active=True).order_by('?')[:50] # Рандомный вывод в слайдер товаров из всей базы.
    context['products'] = products
    context['hotdeals'] = hotdeals
    context['slider_product'] = slider_product
    context['cart'] = cart
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
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    products = Product.objects.filter(is_active=True)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context['products'] = products
    context['cart'] = cart
    return render(request, 'shop/shop.html', context)

def shoplist(request, slug):
    context = {}

    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

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
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    product = get_object_or_404(Product, slug=product_slug)
    albom = ProductAlbomImages.objects.filter(is_active=True, product=product)
    category = product.category
    all_products = Product.objects.all().exclude(slug=product_slug)
    products_from_this_category = Product.objects.filter(category=category)
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