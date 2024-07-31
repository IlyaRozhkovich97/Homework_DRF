from celery import shared_task
from django.core.mail import send_mail
from django.http import BadHeaderError

from config.settings import EMAIL_HOST_USER
from materials.models import Course, Subscription


# тест
@shared_task
def sample_task():
    print("Задача только что была выполнена.")


@shared_task
def send_mail_to_owner(course_id):
    """Функция отправки сообщения об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
        course_subs = Subscription.objects.filter(course=course)
        all_email_list = [sub.user.email for sub in course_subs]

        print(f'Email-адреса для отправки: {all_email_list}')

        if not all_email_list:
            print('Нет подписчиков для отправки email.')
            return

        send_mail(
            subject='Обновление курса',
            message=f'Курс {course.name} был обновлен',
            from_email=EMAIL_HOST_USER,
            recipient_list=all_email_list,
            fail_silently=False,
        )

        print(f'Письма были отправлены на адреса: {", ".join(all_email_list)}')

    except Course.DoesNotExist:
        print(f'Курс с ID {course_id} не найден.')
    except BadHeaderError:
        print('Неправильный заголовок email.')
    except Exception as e:
        print(f'Ошибка при отправке писем: {str(e)}')
