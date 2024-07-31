from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f'Пользователь {user.username} был заблокирован.')
