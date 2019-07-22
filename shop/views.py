from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from info.views import News
from shop.models import Category, Product, ProductAlbomImages, CategoryIndexPage


def index(request):
    context = {}
    cart = request.cart
    products = Product.objects.filter(is_active=True).order_by('?')[:10] # Рандомный вывод 10 товаров на главнй в первом блоке где все товары
    hotdeals = Product.objects.filter(akciya=True).with_rating() # Для вывода рейтинга звезд!
    slider_product = Product.objects.filter(is_active=True).order_by('?')[:50] # Рандомный вывод в слайдер товаров из всей базы.
    news_list = News.objects.filter(is_active=True).order_by('-created')[:5]
    context['cart'] = cart
    context['products'] = products
    context['hotdeals'] = hotdeals
    context['news_list'] = news_list
    context['slider_product'] = slider_product
    context['index_categories'] = CategoryIndexPage.get_index_categories(request.user) # Из модели shop/CategoryIndexPage, выводим в контекст метод get_index_categories()
    return render(request, 'shop/index.html', context)


def products_by_brand(request, pk, slug=None):
    category = get_object_or_404(CategoryIndexPage, pk=pk)
    products = Product.objects.filter(
        is_active=True,
        category__in=category.sortcategory.get_descendants(include_self=True)
    ).order_by('?')
    if slug:
        products = products.filter(brand__slug=slug)
    return render(request, 'shop/index-carousel.html', {'products': products[:10]})


def catlinks(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlinks.html', context)


def catalog(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'shop/catalog.html', {'categories': categories})


def catlist(request, slug):
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlist.html', context)


def shop(request):
    context = {}
    cart = request.cart
    products = Product.objects.filter(is_active=True).with_rating().with_in_wishlist(request.user)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context['products'] = products
    context['cart'] = cart
    return render(request, 'shop/shop.html', context)


def shoplist(request, slug):
    context = {}
    cart = request.cart
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category, is_active=True).with_rating().with_in_wishlist(request.user)
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
    product = get_object_or_404(Product.objects.with_rating().with_in_wishlist(request.user).with_review_count(), slug=product_slug) # Добавил objects.with_rating() и .with_review_count() из модели Product для вывода рейтинга звезд
    albom = ProductAlbomImages.objects.filter(is_active=True, product=product)
    category = product.category
    all_products = Product.objects.all().exclude(slug=product_slug).order_by('?').with_rating().with_in_wishlist(request.user)[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (все товары) .with_rating() - рейтинг звезд
    products_from_this_category = Product.objects.filter(category=category).order_by('?').with_rating().with_in_wishlist(request.user)[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (товары из этой категории) .with_rating() - рейтинг звезд
    hotdeals = Product.objects.filter(akciya=True, timer=True)
    #attribute_and_value = Entry.objects.filter(is_activ=True) # Атрибут и Значение, сейчас работает без вьюхи с models.py с переопределенного кверисета EntryQuerySet
    context['cart'] = cart
    context['albom'] = albom
    context['product'] = product
    context['category'] = category
    context['hotdeals'] = hotdeals
    context['all_products'] = all_products
    context['products_from_this_category'] = products_from_this_category

    #context['attribute_and_value'] = attribute_and_value
    return render(request, 'shop/product-details.html', context)


def modalproduct(request, slug):
    '''Вьюха для вывода товара в модальном окне на главной странице если нажать на товаре кнопку лупы!'''
    context = {}
    modal_product = get_object_or_404(Product, slug=slug)
    context['modal_product'] = modal_product
    return render(request, 'shop/modal-product.html', context)


def compareproducts(request):
    '''Сравнение товаров'''
    return render(request, 'shop/compare.html')


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