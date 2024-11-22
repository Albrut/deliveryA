from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt import views as jwt_views
from .views import CourierLocationView, UserOrdersAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
# urls.py
from django.urls import path
from . import views


schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourdomain.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
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
    path('api/orders/confirm/<int:order_id>/', views.ConfirmOrderView.as_view(), name='confirm-order'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/orders/cancel/<int:order_id>/', views.CancelOrderView.as_view(), name='cancel-order'),
    path('api/courier/location/', CourierLocationView.as_view(), name='courier-location'),
]




