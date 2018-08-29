
from django.shortcuts import render
from shop.models import Category, Brand, Product

def index(request):
    context = {}
    products = Product.objects.filter(is_activ=True)
    brands = Brand.objects.all()
    context['products'] = products
    context['brands'] = brands
    return render(request, 'shop/index.html', context)

def catalog(request):
    categories = Category.objects.filter(is_activ=True)
    return render(request, 'shop/catalog.html', {'categories': categories})

def catlist(request, slug):
    context = {}
    #catlist = Category.objects.filter(is_activ=True)
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    #context['catlist'] = catlist
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlist.html', context )

def shop(request):
    return render(request, 'shop/shop.html')

def shoplist(request):
    return render(request, 'shop/shop-list.html')

def productdetails(request):
    return render(request, 'shop/product-details.html')

def wishlist(request):
    return render(request, 'shop/wishlist.html')

def myaccount(request):
    return render(request, 'shop/my-account.html')

def contact(request):
    return render(request, 'shop/contact.html')

def checkout(request):
    return render(request, 'shop/checkout.html')

def cart(request):
    return render(request, 'shop/cart.html')

def registration(request):
    return render(request, 'shop/registration-account.html')

def about(request):
    return render(request, 'shop/about.html')