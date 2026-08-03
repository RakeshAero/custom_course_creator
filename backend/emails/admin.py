from django.contrib import admin
from .models import EmailLog


# Register your models here.
@admin.register(EmailLog) #equivalent to admin.site.register(EmailLog, EmailLogAdmin)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('email_type', 'recipient', 'subject', 'sent_at', 'status')
    list_filter = ('email_type', 'status', 'created_at')
    search_fields = ('recipient', 'subject')

