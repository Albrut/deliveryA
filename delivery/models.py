from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель User
class User(AbstractUser):
    is_customer = models.BooleanField(default=False)  # Клиент
    is_delivery = models.BooleanField(default=False)  # Доставщик

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
        ('waiting', 'Ожидание'),
        ('in_progress', 'Идёт'),
        ('accepted', 'Принят'),
    ]
    
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)  # Связь с клиентом
    delivery = models.ForeignKey(User, related_name='assigned_orders', null=True, blank=True, on_delete=models.SET_NULL)  # Связь с доставщиком
    product_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    delivery_location = models.CharField(max_length=255, blank=True, null=True)  # Местоположение доставщика

    def __str__(self):
        return f"Заказ {self.product_name} для {self.customer.username}"
