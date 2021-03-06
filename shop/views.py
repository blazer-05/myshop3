from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from info.views import News, Review
from myshop3.settings import MEDIA_URL
from shop.forms import get_filters
from shop.models import Category, Product, ProductAlbomImages, CategoryIndexPage, MiddlwareNotification, PriceList
from notifications.models import Notification

from shop.services import get_categories_by_cookie, get_products_by_cookie, get_attributes, serialize_products


def index(request):
    '''Вывод на главной стр. корзины, акции, главного слайдера, новостей и категорий товаров'''
    context = {}
    cart = request.cart
    #products = Product.objects.filter(is_active=True).order_by('?')[:10] # Рандомный вывод 10 товаров на главнй в первом блоке где все товары
    hotdeals = Product.objects.filter(akciya=True).with_rating() # Для вывода рейтинга звезд!
    slider_product = Product.objects.filter(is_active=True).order_by('?')[:50] # Рандомный вывод в слайдер товаров из всей базы.
    news_list = News.objects.filter(is_active=True).order_by('-created')[:5]
    context['cart'] = cart
    #context['products'] = products
    context['hotdeals'] = hotdeals
    context['news_list'] = news_list
    context['slider_product'] = slider_product
    context['index_categories'] = CategoryIndexPage.get_index_categories(request.user) # Из модели shop/CategoryIndexPage, выводим в контекст метод get_index_categories()
    return render(request, 'shop/index.html', context)


def products_by_brand(request, pk, slug=None):
    '''Получаем категории и товары и сортируем по брендам'''
    category = get_object_or_404(CategoryIndexPage, pk=pk)
    products = Product.objects.filter(
        is_active=True,
        category__in=category.sortcategory.get_descendants(include_self=True)
    ).order_by('?')
    if slug:
        products = products.filter(brand__slug=slug)
    return render(request, 'shop/index-carousel.html', {'products': products[:10]})


def catlinks(request, slug):
    '''Получаем и выводим основные категории товаров'''
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlinks.html', context)


def catalog(request):
    '''Выводим списком весь каталог товаров по категориям'''
    categories = Category.objects.filter(is_active=True)
    return render(request, 'shop/catalog.html', {'categories': categories})


def catlist(request, slug):
    '''Получаем и выводим подкатегории товаров'''
    context = {}
    thiscat = Category.objects.get(slug=slug)
    category_list = thiscat.get_descendants(include_self=True)
    context['thiscat'] = thiscat
    context['category_list'] = category_list
    return render(request, 'shop/catlist.html', context)

# def shop(request):
#     '''Все товары списком без сортировки по категориям'''
#     context = {}
#     cart = request.cart
#     products = Product.objects.filter(is_active=True).with_rating().with_in_wishlist(request.user)
#     paginator = Paginator(products, 10)
#     page = request.GET.get('page')
#     products = paginator.get_page(page)
#     context['products'] = products
#     context['cart'] = cart
#     return render(request, 'shop/shop.html', context)


def shoplist(request, slug):
    '''Получаем и отображаем списком товары принадлежащие данной категории'''
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    '''Для фильтра товаров'''
    form_filters = get_filters(request, products)
    products = form_filters.filter_queryset(products)
    products = products.with_rating().with_in_wishlist(request.user)
    products = form_filters.sort_queryset(products)
    products = form_filters.paginate_queryset(products, request)

    context = {
        'filters': form_filters, # фильтр товаров
        'products': products,
        'category': category,
        'cart': request.cart,

    }
    return render(request, 'shop/shop-list.html', context)


def productdetails(request, product_slug):
    '''Страница детального описания товара(карточка товара). Получаем и выводим на этой странице, товар,
    альбом изображений товара, корзина, категория к которой принадлежит данный товар, все товары, остальные товары из данной категории, акция'''
    context = {}
    cart = request.cart
    product = get_object_or_404(Product.objects.with_rating().with_in_wishlist(request.user).with_review_count(), slug=product_slug) # Добавил objects.with_rating() и .with_review_count() из модели Product для вывода рейтинга звезд
    albom = ProductAlbomImages.objects.filter(is_active=True, product=product)
    category = product.category
    all_products = Product.objects.all().exclude(slug=product_slug).order_by('?').with_rating().with_in_wishlist(request.user)[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (все товары) .with_rating() - рейтинг звезд
    products_from_this_category = Product.objects.filter(category=category).order_by('?').with_rating().with_in_wishlist(request.user)[:10] # Рандомный вывод 10тов.товаров на странице полного описания товара (товары из этой категории) .with_rating() - рейтинг звезд
    hotdeals = Product.objects.filter(akciya=True, timer=True)
    #attribute_and_value = Entry.objects.filter(is_activ=True) # Атрибут и Значение, сейчас работает без вьюхи с models.py с переопределенного кверисета EntryQuerySet

    '''check_for_subscribe - Своего рода фильтр, который смотрит 
    есть ли уже нотификация созданая для этого пользователя, который ждет этот продукт.'''
    check_for_subscribe = MiddlwareNotification.objects.filter(user_name=request.user.pk, product=product).exists()

    '''Если продукт опубликова и пользователь авторизирован на сайте, то получаем нотификацию принадлежащую пользователю
    и продукт этой нотификации и удаляем ее(счетчик на морде сайта обнуляется на 1 после перехода по ссылке из выпадающего списка.)'''
    if product.is_active and request.user.is_authenticated:
        Notification.objects.filter(recipient=request.user, description=product_slug).delete()

    context['cart'] = cart
    context['albom'] = albom
    context['product'] = product
    context['category'] = category
    context['hotdeals'] = hotdeals
    context['all_products'] = all_products
    context['check_for_subscribe'] = check_for_subscribe
    context['products_from_this_category'] = products_from_this_category

    #context['attribute_and_value'] = attribute_and_value
    return render(request, 'shop/product-details.html', context)


def modalproduct(request, slug):
    '''Вьюха для вывода товара в модальном окне на главной странице если нажать на товаре кнопку лупы!'''
    context = {}
    modal_product = get_object_or_404(Product, slug=slug)
    context['modal_product'] = modal_product
    return render(request, 'shop/modal-product.html', context)


def compareproducts(request, category_slug=None):
    '''Сравнение товаров'''
    request.COOKIES.get('compare', '')
    categories = get_categories_by_cookie(request)
    products = get_products_by_cookie(request, category_slug)

    attributes = get_attributes(products)
    context = {
        'categories': categories,
        'products': serialize_products(products),
        'attributes': list(attributes),
    }

    if not category_slug and categories.count() > 1:
        category_slug = categories.first().slug
        return redirect('shop:compare-products-by-category', category_slug=category_slug)

    return render(request, 'shop/compare.html', context=context)


def search(request):
    '''Поиск по товарам'''
    query = request.GET.get('q')

    '''Проверяем, если запрос был (http://localhost:8001/search/) то выводим пустой кверисет'''
    if query:
        search_product = Product.objects.filter(
            Q(title__icontains=query)|
            Q(brand__name__icontains=query)|
            Q(descriptions__icontains=query)|
            Q(category__name__icontains=query)|
            Q(vendor_code__icontains=query)

        )
    else:
        search_product = Product.objects.none()

    count_product = search_product.count()

    paginator = Paginator(search_product, 5)
    page = request.GET.get('page')
    search_product = paginator.get_page(page)

    context = {
        'search_product': search_product,
        'count_product': count_product,
        'query': query,

    }

    return render(request, 'shop/search.html', context)


def notify_create(request):
    '''Создание нотификации'''
    product_slug = request.GET.get('product_slug')
    MiddlwareNotification.objects.create(
        user_name=request.user,
        product=Product.objects.get(slug=product_slug)
        )
    return JsonResponse({
        'created': 'Вы подписались на уведомления о поступлении. Как только товар появится, мы Вам сообщим.'
    })


def price_list_count(request, pk):
    '''Счетчик клика по ссылке скачать прайс лист.'''

    '''Если нужно вывести один прайс-лист то используем этот код без параметра pk!'''
    # try:
    #     price = get_object_or_404(PriceList, is_active=True)
    # except MultipleObjectsReturned:
    #     return HttpResponse('Вы выбрали более одного файла')
    # price.counter += 1
    # price.save()
    # return redirect(price.file.url)

    '''Еслинужно вывести все прайс-листы то используем этот код с параметром pk'''
    price = PriceList.objects.get(pk=pk)
    price.counter += 1
    price.save()
    return redirect(price.file.url)


