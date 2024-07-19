from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserListView, UserRetrieveView, UserUpdateView, UserDeleteView,
                         PaymentViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

app_name = UsersConfig.name

urlpatterns = [
                  path('users/', UserListView.as_view(), name='users-list'),
                  path('register/', UserCreateAPIView.as_view(), name='user-register'),
                  path('users/<int:pk>/', UserRetrieveView.as_view(), name='users-get'),
                  path('users/update/<int:pk>/', UserUpdateView.as_view(), name='users-update'),
                  path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='users-delete'),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + router.urls
