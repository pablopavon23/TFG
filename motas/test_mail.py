from django.core.mail import send_mail
from django.conf import settings

def test_send_mail():
    send_mail('This is a test','The body.',settings.EMAIL_HOST_USER,['pablo_23695@hotmail.es'],fail_silently=False,)
