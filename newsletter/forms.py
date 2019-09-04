from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import NewsletterUser, Newsletter


class NewsletterUserSignUpForm(forms.ModelForm):
    '''Форма email подписки'''

    class Meta:
        model = NewsletterUser
        fields = ['email']

        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control', 'required': False}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'required': True}),
        #
        # }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email


class NewsletterCreationForm(forms.ModelForm):
    '''Форма отправки рассылки'''

    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'users_email', 'file', 'status']

        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'Headline', 'class': 'form-control', 'required': True}),
            'status': forms.Select(attrs={'class': 'form-control','required': True}),
            'file': forms.FileInput(),
            #'users_email': forms.SelectMultiple(attrs={'size': 10, 'class': 'special'}),
            'users_email': forms.CheckboxSelectMultiple(),
            'body': SummernoteWidget(attrs={
                'summernote': {
                    'airMode': False,
                    'width': '100%',
                    'height': '500',
                    # 'toolbar': [
                    #     ['style', ['bold', 'italic', 'underline', 'clear']],
                    #     ['font', ['strikethrough', 'superscript', 'subscript']],
                    #     ['fontsize', ['fontsize']],
                    #     ['color', ['color']],
                    #     ['para', ['ul', 'ol', 'paragraph']],
                    #     ['height', ['height']],
                    #     ['misc', ['codeview']],
                    # ],

                },

            }),

        }


