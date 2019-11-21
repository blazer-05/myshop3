from contacts.models import PrivacyPolicy, HeaderWidgetInfo


def privacy_policy(request):
    '''Политика'''
    privacy_policy = PrivacyPolicy.objects.filter(is_active=True).last()
    return {'privacy_policy': privacy_policy}


def header_widget_info(request):
    '''Виджеты (working time, Free shipping, Money back 100%, Phone:)'''
    widgets = HeaderWidgetInfo.objects.all()
    return {'widgets': widgets}