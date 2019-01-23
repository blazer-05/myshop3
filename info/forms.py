from django import forms
from django.forms import ModelForm
from info.models import Comments

class CommentsForm(forms.ModelForm):
    '''Форма комментариев к статьям'''
    class Meta:
        model = Comments
        fields = ['user_name', 'email', 'text']
        widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'login', 'class':'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder':'e-mail', 'class':'form-control', 'required': False}),
            'text': forms.Textarea(attrs={'placeholder':'message', 'class':'form-control'}),

        }
        # labels = {
        #     'user_name': 'Your name',
        #     'email': 'Your Email',
        #     'text': 'Your Message',
        #
        # }