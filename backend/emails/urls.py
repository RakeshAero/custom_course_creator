from django.urls import path
from .views import email_log

urlpatterns = [
    path('emails/log/', email_log, name='email-log'),
]
