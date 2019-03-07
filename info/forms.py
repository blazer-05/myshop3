from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput
from django.forms import ModelForm
from info.models import Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


# class CustomCaptchaTextInput(CaptchaTextInput):
#     template_name = 'news/custom_field.html'


class CommentForm(forms.ModelForm):
    '''Форма комментариев к статьям без капчи даля авторизованных пользователей'''
    class Meta:
        model = Comment
        fields = ['user', 'user_name', 'email', 'text']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'login', 'class':'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder':'e-mail', 'class':'form-control', 'required': False}),
            #'text': forms.Textarea(attrs={'rows': 5, 'placeholder':'message', 'class':'form-control', 'required': True}),
            'text': SummernoteWidget(attrs={
                'summernote': {
                    'airMode': False,
                    'width': '100%',
                    'height': '300',
                    'toolbar': [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        #['misc', ['codeview']], # кнопка </> исходного кода
                    ],

                },

            }),

        }

        # labels = {
        #     'user_name': 'Your name',
        #     'email': 'Your Email',
        #     'text': 'Your Message',
        #
        # }





class CommentFormCaptcha(forms.ModelForm):
    '''Форма комментариев к статьям с капчей для не авторизованных пользователей'''
    captcha = CaptchaField(label='Are you an human? ',)
    class Meta:
        model = Comment
        fields = ['user', 'user_name', 'email', 'text']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'login', 'class':'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder':'e-mail', 'class':'form-control', 'required': False}),
            #'text': forms.Textarea(attrs={'rows': 5, 'placeholder':'message', 'class':'form-control', 'required': True}),
            'text': SummernoteWidget(attrs={
                'summernote': {
                    'airMode': False,
                    'width': '100%',
                    'height': '300',
                    'toolbar': [
                        ['style', ['bold', 'italic', 'underline', 'clear']],
                        ['font', ['strikethrough', 'superscript', 'subscript']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        #['misc', ['codeview']], # кнопка </> исходного кода
                    ],

                },

            }),
        }