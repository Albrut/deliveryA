from django.db import models
from django.contrib.auth.models import AbstractUser

CITIES = [
    ('Bishkek', 'Bishkek'),
    ('Osh', 'Osh'),
    ('Jalal-Abad', 'Jalal-Abad'),
    ('Karakol', 'Karakol'),
    ('Naryn', 'Naryn'),
    ('Batken', 'Batken'),
    ('Talas', 'Talas'),
    ('Tokmok', 'Tokmok'),
]
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)  # Клиент
    is_delivery = models.BooleanField(default=False)  # Доставщик
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, default='available')

    # Для предотвращения конфликта с родительскими моделями
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='delivery_user_set',  # Уникальное имя для обратной связи
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='delivery_user_permissions_set',  # Уникальное имя для обратной связи
        blank=True
    )

    def __str__(self):
        return self.username


# Модель Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),  # Новый статус
    ]

    product_name = models.CharField(max_length=255)
    customer = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    delivery = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='delivery_orders'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending'
    )
    address = models.TextField()
    delivery_location = models.TextField(default='Default address')
    startpoint = models.CharField(max_length=50, choices=CITIES, default='Bishkek')
    endpoint = models.CharField(max_length=50, choices=CITIES, default='Osh')

    def __str__(self):
        return self.product_name
