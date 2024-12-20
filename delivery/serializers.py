from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Order

# Сериализатор для модели Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product_name', 'status','startpoint', 'endpoint', 'customer']
        read_only_fields = ['customer', 'status']  # Поля, которые нельзя изменить через API

    def create(self, validated_data):
        # Получаем текущего пользователя из контекста
        user = self.context['request'].user
        validated_data['customer'] = user

        # Устанавливаем статус по умолчанию, если не передан
        if 'status' not in validated_data:
            validated_data['status'] = 'pending'

        return Order.objects.create(**validated_data)

    def validate_address(self, value):
        # Пример валидации адреса
        if len(value) < 10:
            raise serializers.ValidationError("Address must be at least 10 characters long.")
        return value


# Сериализатор для регистрации пользователя
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'is_customer', 'is_delivery', 'first_name', 'last_name']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # Убираем ненужное поле

        # Создаем пользователя
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password1'],  # Используем password1
            is_customer=validated_data.get('is_customer', False),
            is_delivery=validated_data.get('is_delivery', False),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            car_type=validated_data.get('car_type', None),
        )
        return user




# Сериализатор для получения данных пользователя
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  # Используем модель пользователя
        fields = '__all__'  # Возвращаем все поля модели

class CourierLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    status = serializers.CharField(max_length=20)