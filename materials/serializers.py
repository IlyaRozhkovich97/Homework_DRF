from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    """
    Класс сериализатора для уроков
    """

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)
        validators = [LessonValidator(field='lesson_url')]


class CourseSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для курсов
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        sub = Subscription.objects.filter(user=user, course=instance)
        if sub.exists():
            return 'Подписка оформлена'
        else:
            return 'Вы не подписаны на курс'
