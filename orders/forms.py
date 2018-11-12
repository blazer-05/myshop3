from django import forms
from django.utils import timezone
from model_utils import Choices

BUYING_TYPE = Choices(
    (0, 'take_out', 'Самовывоз'),
    (1, 'delivery', 'Доставка')
)

class OrderForm(forms.Form):

    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=BUYING_TYPE)
    address = forms.CharField(required=False)
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    comment = forms.CharField(widget=forms.Textarea, required=False)



    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Укажите адрес доставки'
        #self.fields['address'].help_text = '*Обязательно указывайте город!'
        self.fields['comment'].label = 'Комментарий к заказу'
        self.fields['date'].label = 'Дата доставки'
        self.fields['date'].help_text = 'Доставка производится на следущий день после оформления заказа. Менеджер с Вами предварительно свяжется!'

