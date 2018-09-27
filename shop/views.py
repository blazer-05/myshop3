
from django.shortcuts import render, get_object_or_404
from shop.models import Category, Brand, Product, ProductAlbomImages, Attribute, Value, Entry
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def index(request):
    context = {}
    products = Product.objects.filter(is_active=True)
    brands = Brand.objects.all()
    slider_product = Product.objects.filter(is_active=True).order_by('?')[:50] # Рандомный вывод в слайдер товаров из всей базы.
    context['products'] = products
    context['brands'] = brands
    context['slider_product'] = slider_product
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
    categories = Category.objects.filter(is_active=True)
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
    products = Product.objects.filter(is_active=True)
    brands = Brand.objects.all()
    context['products'] = products
    context['brands'] = brands
    return render(request, 'shop/shop.html', context)

def shoplist(request, slug):
    context = {}
    category = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=category, is_active=True)
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
    all_products = Product.objects.all().exclude(slug=product_slug)
    products_from_this_category = Product.objects.filter(category=category)
    #attribute_and_value = Entry.objects.filter(is_activ=True) # Атрибут и Значение, сейчас работает без вьюхи с models.py с переопределенного кверисета EntryQuerySet
    context['product'] = product
    context['albom'] = albom
    context['category'] = category
    context['all_products'] = all_products
    context['products_from_this_category'] = products_from_this_category
    #context['attribute_and_value'] = attribute_and_value
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