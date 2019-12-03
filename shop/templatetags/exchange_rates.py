from django import template
from shop.models import ExchangeRates

register = template.Library()


@register.inclusion_tag('shop/exchange_rates.html')
def store_exchange_rates():
    return {'exchange_rates': ExchangeRates.objects.filter(is_active=True)}