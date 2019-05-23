from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from captcha.fields import CaptchaField


class SignIn(LoginForm):
    captcha = CaptchaField(label='Are you an human? ', )


class SignUp(SignupForm):
    captcha = CaptchaField(label='Are you an human? ', )
    firstname = SignupForm()
    lastname = SignupForm()


