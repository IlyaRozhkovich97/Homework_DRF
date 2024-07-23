from rest_framework.exceptions import ValidationError


class LessonValidator:
    """
    Валидатор для поля ссылки на YouTube
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if 'youtube.com' not in tmp_val:
            raise ValidationError(f'Неверная ссылка в поле {self.field}, она должна содержать youtube.com')
