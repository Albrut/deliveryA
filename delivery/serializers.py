from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Order



# Сериализатор для заказа
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

# Сериализатор для регистрации пользователя
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Использует вашу модель User
        fields = ['username', 'password', 'is_customer', 'is_delivery']  # Включает дополнительные поля

    def create(self, validated_data):
        # Создание пользователя с проверкой пароля
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            is_customer=validated_data.get('is_customer', False),
            is_delivery=validated_data.get('is_delivery', False),
        )
        return user

# Сериализатор для модели User (для получения данных пользователя)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'is_customer', 'is_delivery']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product_name', 'address', 'status', 'delivery_location']

    def create(self, validated_data):
        # Получаем аутентифицированного пользователя
        user = self.context['request'].user

        # Добавляем текущего пользователя как клиента
        validated_data['customer'] = user

        # Если не указан статус, устанавливаем по умолчанию "Ожидание"
        if 'status' not in validated_data:
            validated_data['status'] = 'waiting'
        
        # Создаем заказ
        order = Order.objects.create(**validated_data)
        return order

    def validate_address(self, value):
        # Пример дополнительной валидации для адреса
        if len(value) < 10:
            raise serializers.ValidationError("Address is too short.")
        return value
