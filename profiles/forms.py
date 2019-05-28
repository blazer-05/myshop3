from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from django import forms
from captcha.fields import CaptchaField


class SignIn(LoginForm):
    '''Добавление своих полей в форму авторизации'''
    captcha = CaptchaField(label='Are you an human? ', )


class SignUp(SignupForm):
    '''Добавление своих полей в форму регистрации'''
    captcha = CaptchaField(label='Are you an human? ', )
    first_name = forms.CharField(max_length=30, label='First Name', required=False)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    #phone = forms.CharField(max_length=100, required=False)

    def signup(self, request, user):
        '''Сохранение в базу данных'''
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        #user.phone = self.cleaned_data['phone']
        user.save()
        return user


