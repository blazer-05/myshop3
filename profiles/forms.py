from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from django import forms
from captcha.fields import CaptchaField
from profiles.models import Profile


class SignIn(LoginForm):
    '''Добавление своих полей в форму авторизации'''
    captcha = CaptchaField(label='Are you an human? ', )


class SignUp(SignupForm):
    '''Добавление своих полей в форму регистрации'''
    captcha = CaptchaField(label='Are you an human? ', )
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)


class EditProfileForm(forms.ModelForm):
    '''Редактирование профиля'''

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'date_birth', 'city', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'first_name', 'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'last_name', 'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'phone', 'class': 'form-control', 'required': True}),
            'city': forms.TextInput(attrs={'placeholder': 'city', 'class': 'form-control', 'required': True}),
            'date_birth': forms.DateInput(attrs={'placeholder': 'date_birth', 'class': 'form-control', 'required': True}),
            #'avatar': forms.FileInput(attrs={'placeholder': 'avatar', 'class': 'form-control', 'required': True}),
        }


