from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'description', 'preview_image')
    search_fields = ('name', 'owner__username', 'description')
    list_filter = ('owner',)

    def preview_image(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.preview.url)
        return "No Image"

    preview_image.short_description = 'Изображение Курса'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson_name', 'owner', 'lesson_description', 'lesson_preview_image', 'lesson_url')
    search_fields = ('lesson_name', 'owner__username', 'lesson_description')
    list_filter = ('owner',)

    def lesson_preview_image(self, obj):
        if obj.lesson_preview:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.lesson_preview.url)
        return "No Image"

    lesson_preview_image.short_description = 'Изображение Урока'
