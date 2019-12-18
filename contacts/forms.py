from django import forms
from captcha.fields import CaptchaField
from contacts.models import Contacts, Backcall


class ContactForm(forms.ModelForm):
    '''Форма обратной связи с капчей'''
    captcha = CaptchaField(label='Введите проверочный код ', )

    class Meta:
        model = Contacts
        fields = ['full_name', 'phone', 'email', 'text']

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'required': True}),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your enquiry', 'class': 'form-control', 'required': True}),

        }


class BackcallForm(forms.ModelForm):
    '''Форма обратного звонка с капчей'''
    captcha = CaptchaField(label='Введите проверочный код ', )

    class Meta:
        model = Backcall
        fields = ['full_name', 'phone', 'text']

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone', 'class': 'form-control', 'required': True}),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your enquiry', 'class': 'form-control', 'required': False}),

        }