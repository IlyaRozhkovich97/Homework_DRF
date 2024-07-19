from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    """
    Класс сериализатора для уроков
    """

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('owner',)


class CourseSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для курсов
    """
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('owner',)

    @staticmethod
    def get_lessons_count(obj):
        return obj.lessons.count()
