from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Order, User
from .serializers import OrderSerializer, UserSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import status


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
