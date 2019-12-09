from django.utils.deprecation import MiddlewareMixin

from shop.models import ExchangeRates


class ExchangeRate(MiddlewareMixin):
    def process_request(self, request):
        exchange_rate_id = request.session.get('exchange_rate')

        current_exchange_rate = None
        if exchange_rate_id:
            current_exchange_rate = ExchangeRates.objects.filter(
                pk=exchange_rate_id,
                is_active=True
            ).first()

        exchange_rate_default = ExchangeRates.default_currency()

        request.exchange_rate = current_exchange_rate or exchange_rate_default
        request.exchange_rate_default = exchange_rate_default
