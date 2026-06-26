from django import forms

class Client(forms.Form):
    name = forms.CharField(max_length=20, min_length=2, label="Введіть ім'я")
    last_name = forms.CharField(max_length=100, min_length=2, label="Введіть прізвище")
    phone = forms.CharField(min_length=5, max_length=15, label="Номер телефону")
    email = forms.EmailField(max_length=100, min_length=5, label="Email")
    country = forms.CharField(max_length=100, min_length=2, label="Країна")
    city = forms.CharField(max_length=50, min_length=2, label="Населений пункт")
    street = forms.CharField(max_length=100, min_length=2, label="Вулиця")
    building = forms.CharField(max_length=10, min_length=1, label="Будинок")
    office = forms.CharField(max_length=10, min_length=1, label="Квартира/офіс")
    entrance = forms.CharField(max_length=50, min_length=1, label="Під'їзд")
    region = forms.CharField(max_length=50, min_length=2, label="Область/штат")
    zip_code = forms.CharField(max_length=20, min_length=3, label="Індекс")