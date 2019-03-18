
from django import template
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string

from comments.models import Comment
from comments.forms import CommentForm, CommentFormCaptcha

register = template.Library()

@register.inclusion_tag('add_comments.html')
def add_comment(newsdetails, request):

    form_initial = {'content_type': ContentType.objects.get_for_model(newsdetails), 'object_id': newsdetails.pk}
    comments = Comment.objects.filter(is_active=True, **form_initial).order_by('-created')

    all_comment = comments.count()

    paginator = Paginator(comments, 5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    if not request.user.is_authenticated:
        form = CommentFormCaptcha(initial=form_initial)  # Форма с капчей
    else:
        form = CommentForm(initial=form_initial)  # Форма без капчи


    return {'comments': comments,
            'all_comment': all_comment,
            'form': form,
            #'form_user ': form_user,
            'request': request,
            }



