from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from materials.models import Course, Lesson, Subscription
from users.models import User


class TestLessons(APITestCase):
    """ Тестирование уроков """

    def setUp(self) -> None:
        self.user = User.objects.create(email="admin@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="Python", description="Основы Python")
        self.lesson = Lesson.objects.create(
            course=self.course,
            lesson_name="Основы backend-разработки",
            lesson_description="Это создание скрытой от пользователя серверной части приложения, то есть логики сайта",
            owner=self.user,
            lesson_url="https://www.youtube.com/watch",
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """

        url = reverse("materials:lesson-create")
        data = {
            "lesson_name": "Основы backend-разработки",
            "lesson_description": "Это создание скрытой от пользователя серверной части приложения, то есть "
                                  "логики сайта",
            "course": self.course.id,
            "lesson_url": "https://www.youtube.com/watch",
        }

        response = self.client.post(url, data=data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(data.get("lesson_name"), "Основы backend-разработки")
        self.assertEqual(data.get("course"), self.course.id)
        self.assertEqual(data.get("lesson_url"), "https://www.youtube.com/watch")
        self.assertEqual(data.get("lesson_description"), "Это создание скрытой от пользователя серверной "
                                                         "части приложения, то есть логики сайта")

    def test_update_lesson(self):
        """ Тестирование изменений урока """

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "lesson_name": "Основы backend-разработки",
            "lesson_description": "Это создание скрытой от пользователя серверной части приложения, "
                                  "то есть логики сайта",
            "course": self.lesson.course.id,
            "lesson_url": "https://www.youtube.com/watch",
        }
        response = self.client.put(url, data)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("lesson_name"), self.lesson.lesson_name)
        self.assertEqual(data.get("lesson_description"), "Это создание скрытой от пользователя серверной части "
                                                         "приложения, то есть логики сайта")
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("owner"), self.lesson.owner.id)

    def test_retrieve_lesson(self):
        """ Тестирование просмотра одного урока """

        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("lesson_name"), self.lesson.lesson_name)
        self.assertEqual(data.get("lesson_description"), self.lesson.lesson_description)
        self.assertEqual(data.get("course"), self.lesson.course.id)
        self.assertEqual(data.get("owner"), self.lesson.owner.id)

    def test_delete_lesson(self):
        """ Тестирование удаления  урока """

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    """ Тестирование подписок """

    def setUp(self):
        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(name="Основы backend-разработки",
                                            description="Это создание скрытой от пользователя "
                                                        "серверной части приложения, то есть логики сайта")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("materials:set_subscribe", args=[self.course.id])

    def test_subscription_activate(self):
        """Тестирование активации подписки"""
        data = {"user": self.user.id, "course": self.course.id}
        response = self.client.post(self.url, data=data, format='json')
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), 1)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
        self.assertEqual(response.json().get("message"), "подписка добавлена")
