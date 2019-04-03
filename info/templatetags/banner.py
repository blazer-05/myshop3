from django import template
from info.models import Banners

register=template.Library()


@register.inclusion_tag('info/top_left_banner_tpl.html')
def top_left_banner():
    banners = Banners.objects.get(id=4)
    return {'banners': banners}


@register.inclusion_tag('info/top_right_banner_tpl.html')
def top_right_banner():
    banners = Banners.objects.get(id=5)
    return {'banners': banners}


@register.inclusion_tag('info/bottom_left_banner_tpl.html')
def bottom_left_banner():
    banners = Banners.objects.get(id=6)
    return {'banners': banners}


@register.inclusion_tag('info/bottom_right_banner_tpl.html')
def bottom_right_banner():
    banners = Banners.objects.get(id=7)
    return {'banners': banners}


@register.inclusion_tag('info/center_big_banner_tpl.html')
def center_big_banner():
    banners = Banners.objects.get(id=8)
    return {'banners': banners}


@register.inclusion_tag('info/left_block_banner_tpl.html')
def left_block_banner():
    '''Вывод в index.html двойного баннера Нокиа в левом сайдбаре!'''
    context = {}
    nokia_one = Banners.objects.get(id=1)
    nokia_two = Banners.objects.get(id=2)
    context['nokia_one'] = nokia_one
    context['nokia_two'] = nokia_two
    return context