from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner, IsAdminUser

"""Course"""


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Этот ViewSet предоставляет действия 'list', 'create', 'retrieve', 'update' и 'destroy'.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            # Разрешить создание курсов всем аутентифицированным пользователям
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            # Удаление доступно только владельцам или администраторам
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['update', 'retrieve']:
            # Обновление и получение информации доступны модераторам, администраторам и владельцам
            permission_classes = [IsAuthenticated, IsModerator | IsAdminUser | IsOwner]
        elif self.action == 'list':
            # Просмотр списка доступен всем аутентифицированным пользователям
            permission_classes = [IsAuthenticated]
        else:
            # По умолчанию доступен всем аутентифицированным пользователям
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


"""Lesson"""


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.user.groups.filter(name='Moderators').exists():
            # Модератор может создавать уроки
            permission_classes = [IsAuthenticated]
        else:
            # Только администратор может создавать уроки
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя в поле owner
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение списка сущностей.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение одной сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator, IsAdminUser | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsAdminUser | IsOwner]
