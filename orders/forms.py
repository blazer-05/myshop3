from django import forms
from django.utils import timezone
from model_utils import Choices

BUYING_TYPE = Choices(
    ('take_out', 'Самовывоз'),
    ('delivery', 'Доставка'),
)


class OrderForm(forms.Form):
    full_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=BUYING_TYPE)
    address = forms.CharField(required=False)
    delivery_date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = '*ФИО'
        self.fields['phone'].label = '*Контактный телефон'
        self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться'
        self.fields['email'].label = 'Ваш e-mail на него придет копия заказа'
        self.fields['email'].help_text = 'Ваш e-mail адрес'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Укажите адрес доставки'
        self.fields['address'].help_text = '*Обязательно указывайте город, почтовый индекс, улица, дом, квартира!'
        self.fields['comment'].label = 'Комментарий к заказу'
        self.fields['delivery_date'].label = 'Дата доставки'
        self.fields['delivery_date'].help_text = 'Доставка производится на следущий день после оформления заказа. Менеджер с Вами предварительно свяжется!'

