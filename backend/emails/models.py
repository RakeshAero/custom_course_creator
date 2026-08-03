from django.db import models
from users.models import User

class EmailLog(models.Model):

    #Constants
    TYPE_WELCOME = 'welcome'
    TYPE_WEEKLY = 'weekly'
    TYPE_CHOICES = [
        (TYPE_WELCOME, 'Welcome Email'),
        (TYPE_WEEKLY, 'Weekly Email'),
    ]

    #Delivery Status Constants
    STATUS_QUEUED = 'queued'
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [
        (STATUS_QUEUED, 'Queued'),
        (STATUS_SENT, 'Sent'),
        (STATUS_FAILED, 'Failed'),
    ]

    #Fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.EmailField()
    email_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_QUEUED)
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True) # when it was queued
    sent_at = models.DateTimeField(null=True, blank=True)  # when it actually went out

    class Meta:
        ordering = ['-created_at']  # Newest first

    def __str__(self):
        return f"{self.email_type} -> {self.recipient} [{self.status}]"