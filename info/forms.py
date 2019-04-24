from django import forms
from info.models import Review
from captcha.fields import CaptchaField


class ReviewForm(forms.ModelForm):
    '''Форма создания отзыва без капчи'''
    class Meta:
        model = Review
        fields = ['user_name', 'product', 'city', 'image', 'merits', 'limitations', 'comment',
                  'email', 'video', 'rating', 'period']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Nickname*', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'required': False}),
            'city': forms.TextInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'merits': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your merits', 'class': 'form-control', 'required': True}),
            'limitations': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your limitations', 'class': 'form-control', 'required': True}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your comment', 'class': 'form-control', 'required': True}),
            #'image': forms.FileInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'video': forms.URLInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'period': forms.Select(attrs={'class': 'form-control','required': True}),
            'product': forms.HiddenInput()

        }


class ReviewFormCaptcha(forms.ModelForm):
    '''Форма создания отзыва с капчей'''
    captcha = CaptchaField(label='Are you an human? ', )

    class Meta:
        model = Review
        fields = ['user_name', 'product', 'city', 'image', 'merits', 'limitations', 'comment',
                  'email', 'video', 'rating', 'period']

        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Nickname*', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'required': False}),
            'city': forms.TextInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'merits': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your merits', 'class': 'form-control', 'required': True}),
            'limitations': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your limitations', 'class': 'form-control', 'required': True}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your comment', 'class': 'form-control', 'required': True}),
            #'image': forms.FileInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'video': forms.URLInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'period': forms.Select(attrs={'class': 'form-control','required': True}),
            'product': forms.HiddenInput()

        }


class EditReviewForm(forms.ModelForm):
    '''Форма редактирования отзыва'''
    class Meta:
        model = Review
        fields = ['user_name', 'product', 'city', 'image', 'merits', 'limitations', 'comment',
                  'email', 'video', 'rating', 'period']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder': 'Nickname*', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control', 'required': False}),
            'city': forms.TextInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'merits': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your merits', 'class': 'form-control', 'required': True}),
            'limitations': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your limitations', 'class': 'form-control', 'required': True}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Please enter your comment', 'class': 'form-control', 'required': True}),
            #'image': forms.FileInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'video': forms.URLInput(attrs={'placeholder': 'Please enter your city', 'class': 'form-control', 'required': False}),
            'period': forms.Select(attrs={'class': 'form-control','required': True}),
            'product': forms.HiddenInput()

        }