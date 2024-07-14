from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import (UserListView, UserCreateAPIView, UserRetrieveView, UserUpdateView,
                         UserDeleteView, PaymentViewSet)


router = DefaultRouter()
router.register(r'payment', PaymentViewSet, basename='payment')

app_name = UsersConfig.name

urlpatterns = [
                  path('users/', UserListView.as_view(), name='users-list'),
                  path('users/create/', UserCreateAPIView.as_view(), name='users-create'),
                  path('users/<int:pk>/', UserRetrieveView.as_view(), name='users-get'),
                  path('users/update/<int:pk>/', UserUpdateView.as_view(), name='users-update'),
                  path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='users-delete'),
              ] + router.urls
