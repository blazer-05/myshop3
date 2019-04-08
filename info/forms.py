from django import forms
from info.models import Review
from captcha.fields import CaptchaField


class ReviewForm(forms.ModelForm):
    '''Форма создания отзыва без капчи'''
    class Meta:
        model = Review
        fields = ['user', 'user_name', 'city', 'image', 'merits', 'limitations', 'comment',
                  'email', 'video', 'rating', 'period', 'user_like', 'user_dislike']


class ReviewFormCaptcha(forms.ModelForm):
    '''Форма создания отзыва с капчей'''
    captcha = CaptchaField(label='Are you an human? ', )

    class Meta:
        model = Review
        fields = ['user', 'user_name', 'city', 'image', 'merits', 'limitations', 'comment',
                  'email', 'video', 'rating', 'period', 'user_like', 'user_dislike']

