from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {'blank': True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    session_id = models.CharField(max_length=255, verbose_name='id_сессии', null=True, blank=True)
    link = models.URLField(max_length=400, verbose_name='ссылка на оплату', null=True, blank=True)

    def __str__(self):
        return f'{self.user} за {self.course if self.course else self.lesson}, {self.amount} руб. ({self.date})'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
