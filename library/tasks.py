from celery import shared_task

from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(text, email):
    django_send_mail("Reminder", text, 'admin@example.com', [email])
