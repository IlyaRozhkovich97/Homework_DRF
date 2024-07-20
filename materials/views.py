from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner

"""Course"""


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Этот ViewSet предоставляет действия 'list', 'create', 'retrieve', 'update' и 'destroy'.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~IsModerator, IsAuthenticated,)
        elif self.action == 'destroy':
            self.permission_classes = (~IsModerator, IsOwner,)
        elif self.action in ['update', 'list', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()


"""Lesson"""


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение списка сущностей.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение одной сущности.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = Lesson.objects.all()
    permission_classes = (~IsModerator, IsOwner)
