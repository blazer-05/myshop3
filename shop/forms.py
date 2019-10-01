from collections import defaultdict

from django import forms
from django.db.models import Prefetch, Q, Min, Max, IntegerField
from django.db.models.functions import Cast

from shop.models import Brand, Value, Attribute


'''Фильтр товаров'''


class FilterCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'shop/widgets/checkbox_select.html'

    '''Для использования другого стиля фильтра товаров нужно расскомментировать эту option_template_name строку и 
    в шаблоне checkbox_select.html закомментировать первый html код и расскоментировать второй html код'''
    #option_template_name = 'shop/widgets/checkbox_option.html'


class ProductFilter(forms.Form):
    min_price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    brand = forms.MultipleChoiceField(choices=[], required=False, widget=FilterCheckboxSelectMultiple())
    filter = forms.MultipleChoiceField(choices=[], required=False, widget=FilterCheckboxSelectMultiple())

    def __init__(self, products, initial_min_price, initial_max_price, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_min_price = initial_min_price
        self.initial_max_price = initial_max_price
        self.fields['filter'].choices = self.__get_filter_choices(products)
        self.fields['brand'].choices = self.__get_brand_choices(products)

    @staticmethod
    def __get_brand_choices(products):
        return [(
            'brands',
            list(Brand.objects.filter(product__in=products).distinct().values_list('id', 'name'))
        )]

    @staticmethod
    def __get_filter_choices(products):
        attributes = Attribute.objects.filter(
            is_filter=True,
            entry__product__in=products
        ).prefetch_related(
            Prefetch(
                'value_set',
                Value.objects.filter(entry__product__in=products).distinct()
            )
        ).distinct()

        choices = []
        for attr in attributes:
            choices.append((
                attr.title,
                [(o.id, o.value) for o in attr.value_set.all()]
            ))
        return choices

    def filter_queryset(self, queryset):
        if not self.is_valid():
            return queryset.none()

        brand = self.cleaned_data.get('brand')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')
        value = self.cleaned_data.get('filter')

        if brand:
            queryset = queryset.filter(brand__in=brand)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if value:
            q = defaultdict(list)
            for attribute, pk in Value.objects.filter(pk__in=value).values_list('attribute', 'pk'):
                q[attribute].append(pk)

            for pks in q.values():
                queryset = queryset.filter(entry__value__in=pks)

        return queryset


def get_filters(request, products):
    initial = products.aggregate(
        min_price=Cast(Min('price'), output_field=IntegerField()),
        max_price=Cast(Max('price'), output_field=IntegerField())
    )
    initial_min_price = initial.get('min_price')
    initial_max_price = initial.get('max_price')
    form_data = {
        'products': products,
        'initial_min_price': initial_min_price,
        'initial_max_price': initial_max_price,
    }
    if 'min_price' in request.GET:
        return ProductFilter(**form_data, data=request.GET)
    return ProductFilter(**form_data, data=initial)