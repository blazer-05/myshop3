
from django.shortcuts import render, get_object_or_404
from shop.models import Category, Brand, Product, ProductAlbomImages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def index(request):
    context = {}
    products = Product.objects.filter(is_activ=True)
    brands = Brand.objects.all()
    context['products'] = products
    context['brands'] = brands
    return render(request, 'shop/index.html', context)

def catlinks(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    #product = Product.objects.all()
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    #context['product'] = product
    return render(request, 'shop/catlinks.html', context )

def catalog(request):
    categories = Category.objects.filter(is_activ=True)
    return render(request, 'shop/catalog.html', {'categories': categories})

def catlist(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    #product = Product.objects.all()
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    #context['product'] = product
    return render(request, 'shop/catlist.html', context )

def shop(request):
    context = {}
    products = Product.objects.filter(is_activ=True)
    brands = Brand.objects.all()
    context['products'] = products
    context['brands'] = brands
    return render(request, 'shop/shop.html', context)

def shoplist(request, slug):
    context = {}
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category, is_activ=True)
    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context['category'] = category
    context['product'] = product
    return render(request, 'shop/shop-list.html', context)

def productdetails(request, product_slug, albom_id):
    context = {}
    product = get_object_or_404(Product, slug=product_slug)
    albom = ProductAlbomImages.objects.filter(product=albom_id)
    category = product.category
    top_five_products = Product.objects.all().exclude(slug=product_slug)
    top_five_products_category = Product.objects.filter(category=category)
    context['product'] = product
    context['albom'] = albom
    context['category'] = category
    context['top_five_products'] = top_five_products
    context['top_five_products_category'] = top_five_products_category
    print(dir(product))
    return render(request, 'shop/product-details.html', context)

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