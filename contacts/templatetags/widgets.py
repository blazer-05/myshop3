from django import template
from contacts.models import HeaderWidgetInfo

register = template.Library()


@register.inclusion_tag('header_info.html')
def header_widget_info():
    '''Виджеты (working time, Free shipping, Money back 100%, Phone:)'''
    widgets = HeaderWidgetInfo.objects.all()
    return {'widgets': widgets}