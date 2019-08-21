from django import forms
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
        fields = ['subject', 'body', 'email', 'status']
