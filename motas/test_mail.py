from django.core.mail import send_mail
from django.conf import settings

def test_send_mail(cuerpo_mail):
    send_mail('Valores anómalos info',cuerpo_mail,settings.EMAIL_HOST_USER,[''],fail_silently=False,)
