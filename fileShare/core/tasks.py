from celery import shared_task
import os
from django.core.mail import send_mail 
@shared_task
def sendVerificationMail(email,token):
    try:
        
        link = f"http://{os.environ.get('DOMAIN')}/verify-email/{token}/"
        print("sentding mail")
        send_mail(
        "Verify your account",
        f"Click the link to verify your account: {link}",
        "bhardwajvaibhav2412@gmail.com",
        [email]
        )
        print("sent mail")
    except Exception as e:
        print(e)