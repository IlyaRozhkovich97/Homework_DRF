from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from materials.models import Course, Lesson, Subscription
from materials.paginations import MaterialsPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner
from materials.tasks import send_mail_to_owner


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Course.
    Этот ViewSet предоставляет действия 'list', 'create', 'retrieve', 'update' и 'destroy'.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsModerator | IsOwner]
        elif self.action in ['update', 'list', 'retrieve']:
            permission_classes = [IsModerator | IsOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        course = serializer.save()
        send_mail_to_owner.delay(course.id)
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за создание сущности.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsModerator | IsOwner]
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Базовый класс Generic-классов, отвечающий за отображение одной сущности.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Базовый класс Generic-классов, отвечающий за редактирование сущности.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Базовый класс Generic-классов, отвечающий за удаление сущности.
    """
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class SetSubscription(APIView):
    """
    Класс для управления подписками пользователя на курсы.
    """

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.kwargs['pk']
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            return Response({"message": "подписка удалена"}, status=status.HTTP_204_NO_CONTENT)
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            return Response({"message": "подписка добавлена"}, status=status.HTTP_201_CREATED)
