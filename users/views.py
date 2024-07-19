from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer

"""Payment"""


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date',)


"""User"""


class UserListView(generics.ListAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение списка сущностей.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        obj = serializer.save(is_active=True)
        obj.set_password(self.request.data['password'])
        obj.save()


class UserRetrieveView(generics.RetrieveAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение одной сущности.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserUpdateView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
