from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Order

# Форма для регистрации
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_customer', 'is_delivery']

# Форма для авторизации
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# Форма для создания заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product_name', 'address']

# Форма для принятия заказа доставщиком
class AcceptOrderForm(forms.Form):
    order_id = forms.IntegerField()

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Order

# Форма для регистрации
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_customer', 'is_delivery']

# Форма для авторизации
class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']