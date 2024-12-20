from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Order, User
from .serializers import CourierLocationSerializer, OrderSerializer, UserSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import status
from rest_framework.exceptions import PermissionDenied


# API для заказов
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут создавать заказы

    def perform_create(self, serializer):
        # Устанавливаем заказ для текущего пользователя
        serializer.save(customer=self.request.user)

        def get_queryset(self):
        # Возвращаем заказы только текущего пользователя
            user = self.request.user
            if user.is_customer:
                return Order.objects.filter(customer=user)  # Заказы, где пользователь — клиент
            elif user.is_delivery:
                return Order.objects.filter(delivery=user)  # Заказы, где пользователь — доставщик
            return Order.objects.none()  # Для других случаев


# API для пользователей
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Регистрация пользователя (API)
class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


# Логин пользователя (API)
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return Response({"detail": "Login successful"})
        else:
            return Response({"detail": "Invalid credentials"}, status=400)


# API для принятия заказа
class AcceptOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=404)

        if order.delivery is not None:
            return Response({"detail": "Order already accepted"}, status=400)

        # Назначаем доставщика
        order.delivery = request.user
        order.status = 'in_progress'
        order.save()
        return Response({"detail": "Order accepted"}, status=200)


class CreateOrderAPIView(APIView):
    permission_classes = []   # Только для аутентифицированных пользователей

    def post(self, request, *args, **kwargs):
        # Создаем сериализатор с данными запроса
        serializer = OrderSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Сохраняем заказ, если данные валидны
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    from .models import Order
    from .serializers import OrderSerializer
class UserOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Фильтруем заказы, где пользователь — клиент
        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, является ли текущий пользователь назначенным доставщиком
        if order.delivery != request.user:
            return Response({"detail": "You are not the assigned delivery person for this order."}, status=status.HTTP_403_FORBIDDEN)

        # Если статус заказа 'in_progress', меняем его на 'accepted'
        if order.status == 'in_progress':
            order.status = 'accepted'  # Меняем статус на "accepted"
            order.save()
            return Response({"detail": "Order confirmed and accepted."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Order is not in progress."}, status=status.HTTP_400_BAD_REQUEST)
        

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, может ли пользователь отменить заказ
        if order.customer != request.user and not request.user.is_staff:
            raise PermissionDenied("You do not have permission to cancel this order.")

        # Изменяем статус заказа на 'canceled'
        if order.status in ['pending', 'in_progress']:
            order.status = 'canceled'
            order.save()
            return Response({"detail": "Order has been canceled."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Order cannot be canceled in its current state."}, status=status.HTTP_400_BAD_REQUEST)

class CourierLocationView(APIView):
    permission_classes = [IsAuthenticated]  # Доступ для всех аутентифицированных пользователей

    def get(self, request, *args, **kwargs):
        # Получаем все заказы, где клиент — это текущий пользователь
        orders = Order.objects.filter(customer=request.user, status='in_progress')

        if not orders.exists():
            return Response({"detail": "No orders in progress for your account."}, status=status.HTTP_404_NOT_FOUND)

        # Заказы с назначенным курьером
        courier_location_data = []
        for order in orders:
            if order.delivery:
                courier = order.delivery  # Курьер, который доставляет заказ
                courier_location_data.append({
                    'order_id': order.id,
                    'courier_username': courier.username,
                    'latitude': courier.latitude,
                    'longitude': courier.longitude,
                    'status': courier.status  # Статус курьера: "in_progress", "available" и т.д.
                })
            else:
                courier_location_data.append({
                    'order_id': order.id,
                    'courier': None,
                    'message': 'No courier assigned yet.'
                })

        return Response(courier_location_data)

    def post(self, request, *args, **kwargs):
        # Проверяем, является ли пользователь курьером для обновления местоположения
        if not request.user.is_delivery:
            return Response({"detail": "You are not authorized to update this information."}, status=status.HTTP_403_FORBIDDEN)
        
        # Получаем данные из запроса
        serializer = CourierLocationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Обновляем местоположение курьера
            request.user.latitude = serializer.validated_data['latitude']
            request.user.longitude = serializer.validated_data['longitude']
            request.user.status = serializer.validated_data['status']
            request.user.save()

            return Response({"detail": "Courier location updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Только для аутентифицированных пользователей
    authentication_classes = [JWTAuthentication]  # Используем JWT аутентификацию

    def get(self, request, *args, **kwargs):
        # Используем сериализатор для возврата всех полей пользователя
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer

class CourierOrdersAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает все заказы.
        """
        return Order.objects.all()
