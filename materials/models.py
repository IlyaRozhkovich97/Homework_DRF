from django.db import models


class Course(models.Model):
    """
    Модель курса, содержит поля: название курса, изображение курса, описание курса и владелец курса
    """
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='media/course_previews/', verbose_name='изображение курса', null=True,
                                blank=True)
    description = models.TextField(verbose_name='описание курса', null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец курса', blank=True,
                              null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    """
    Модель урока, содержит поля: название урока, описание урока, изображение урока, ссылка на видео и владелец урока
    """
    lesson_name = models.CharField(max_length=100, verbose_name='название урока')
    lesson_description = models.TextField(verbose_name='описание урока', null=True, blank=True)
    lesson_preview = models.ImageField(upload_to='media/lesson_previews/', verbose_name='изображение урока', null=True,
                                       blank=True)
    lesson_url = models.CharField(max_length=300, verbose_name='ссылка на видео', null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец урока', blank=True,
                              null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курс')

    def __str__(self):
        return self.lesson_name

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
