from django import forms

class Client(forms.Form):
    name = forms.CharField(max_length=20, min_length=2, label="Введіть ім'я")
    last_name = forms.CharField(max_length=100, min_length=2, label="Введіть прізвище")
    phone = forms.CharField(min_length=5, max_length=15, label="Номер телефону")
    email = forms.EmailField(max_length=20, min_length=5, label="Email")