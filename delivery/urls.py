from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import UserOrdersAPIView

# urls.py
from django.urls import path
from . import views

# Создаём роутер для API
router = DefaultRouter()

router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('api/login/', views.UserLoginAPIView.as_view(), name='login'),
    path('api/orders/accept/<int:order_id>/', views.AcceptOrderView.as_view(), name='accept-order'),
    path('api/orders/create/', views.CreateOrderAPIView.as_view(), name='create-order'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/orders/user/', UserOrdersAPIView.as_view(), name='user-orders'),
]



