from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Этот ViewSet предоставляет действия 'list', 'create', 'retrieve', 'update' и 'destroy'.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение списка сущностей.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение одной сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = Lesson.objects.all()
