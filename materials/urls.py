from django.urls import path
from rest_framework.routers import DefaultRouter
from .apps import MaterialsConfig
from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonUpdateAPIView,
                    LessonRetrieveAPIView, LessonListAPIView, SetSubscription)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")

app_name = MaterialsConfig.name

urlpatterns = [
                  path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),
                  path('subscribe/<int:pk>/', SetSubscription.as_view(), name='set_subscribe'),
              ] + router.urls
