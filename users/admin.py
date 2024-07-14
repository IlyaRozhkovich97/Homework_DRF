from django.contrib import admin
from .models import User, Payment


# Регистрация модели User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'avatar', 'country', 'city')
    search_fields = ('email', 'phone', 'country', 'city')
    list_filter = ('country', 'city')


# Регистрация модели Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course', 'lesson', 'amount', 'payment_method')
    search_fields = ('user__email', 'course__name', 'lesson__lesson_name')
    list_filter = ('payment_method',)
