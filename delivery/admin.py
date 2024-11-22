# admin.py
from django.contrib import admin
from .models import User, Order

# Регистрация модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_delivery')  # Укажите поля для отображения
    list_filter = ('is_customer', 'is_delivery')  # Фильтрация по ролям
    search_fields = ('username', 'email')  # Поиск по имени пользователя и email

# Регистрация модели Order
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'customer', 'delivery', 'status', 'address', 'delivery_location')  # Отображаемые поля
    list_filter = ('status', 'customer', 'delivery')  # Фильтрация по статусу, клиенту и доставщику
    search_fields = ('product_name', 'customer__username')  # Поиск по продукту и имени клиента

