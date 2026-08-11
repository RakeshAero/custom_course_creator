from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import EmailLog
from .serializers import EmailLogSerializer

#Display a Delivery Rate (Average) of Emails sent
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def email_log(request):
    """
    GET /api/emails/log/  (instructor/admin only)
    Returns delivery stats + the most recent email log rows.
    """
    if request.user.role not in ('instructor', 'admin'):
        return Response(
            {'error': 'Instructor or admin access required.'},
            status=status.HTTP_403_FORBIDDEN
            )
    total = EmailLog.objects.count()
    sent = EmailLog.objects.filter(status=EmailLog.STATUS_SENT).count()
    failed = EmailLog.objects.filter(status=EmailLog.STATUS_FAILED).count()
    queued = EmailLog.objects.filter(status=EmailLog.STATUS_QUEUED).count()

     # Metric 4: % of emails successfully sent vs total
    delivery_rate = round(( sent / total ) * 100) if total else 0

    logs = EmailLog.objects.all()[:100] # newest first (model Meta ordering)


    return Response({
        'delivery_rate' : delivery_rate,
        'total' : total,
        'sent' : sent,
        'failed' : failed,
        'queued' : queued,
        'logs' : EmailLogSerializer(logs, many=True).data,
    })