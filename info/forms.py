from django import forms
from django.forms import ModelForm
from info.models import Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class CommentForm(forms.ModelForm):
    '''Форма комментариев к статьям'''
    class Meta:
        model = Comment
        fields = ['user', 'user_name', 'email', 'text']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'login', 'class':'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder':'e-mail', 'class':'form-control', 'required': False}),
            'text': forms.Textarea(attrs={'placeholder':'message', 'class':'form-control', 'required': True}),

        }
        # labels = {
        #     'user_name': 'Your name',
        #     'email': 'Your Email',
        #     'text': 'Your Message',
        #
        # }

