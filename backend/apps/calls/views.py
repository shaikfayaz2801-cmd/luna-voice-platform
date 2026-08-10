"""
Calls views — call initiation, history, Twilio webhooks.
"""
import logging
import uuid
from django.http import HttpResponse
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Call, CallLog
from .serializers import CallSerializer, CallLogSerializer
from .twilio_handler import generate_twiml_connect, generate_twiml_say, initiate_outbound_call

logger = logging.getLogger(__name__)


class CallListView(generics.ListAPIView):
    """List all calls for the authenticated user."""
    serializer_class = CallSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Call.objects.filter(user=self.request.user).order_by('-started_at')


class CallDetailView(generics.RetrieveAPIView):
    """Get call details including logs."""
    serializer_class = CallSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Call.objects.filter(user=self.request.user)


class CallLogsView(generics.ListAPIView):
    """List call transcript logs for a specific call."""
    serializer_class = CallLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CallLog.objects.filter(
            call_id=self.kwargs['call_id'],
            call__user=self.request.user
        ).order_by('timestamp')


class InitiateCallView(views.APIView):
    """Initiate an outbound call via Twilio."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number', '').strip()
        if not phone_number:
            return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        result = initiate_outbound_call(to=phone_number, user=request.user)

        if 'error' in result:
            return Response({'error': result['error']}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Create call record
        call = Call.objects.create(
            user=request.user,
            call_sid=result['call_sid'],
            direction='outbound',
            phone_number=phone_number,
            status=result.get('status', 'initiated'),
        )

        return Response(CallSerializer(call).data, status=status.HTTP_201_CREATED)


class TwilioWebhookView(views.APIView):
    """
    Twilio webhook — called when an inbound call arrives.
    Returns TwiML to connect the call to our Media Stream WebSocket.
    No authentication required (Twilio signs requests).
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        call_sid = request.POST.get('CallSid', '')
        from_number = request.POST.get('From', '')
        to_number = request.POST.get('To', '')

        # Create or get the call record
        call, _ = Call.objects.get_or_create(
            call_sid=call_sid,
            defaults={
                'user_id': None,  # Inbound from unknown user
                'direction': 'inbound',
                'phone_number': from_number,
                'status': 'in-progress',
            }
        )

        twiml = generate_twiml_connect(call_sid)
        return HttpResponse(twiml, content_type='application/xml')


class TwilioStatusCallbackView(views.APIView):
    """Twilio status callback — updates call status in DB."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        call_sid = request.POST.get('CallSid', '')
        call_status = request.POST.get('CallStatus', '')
        duration = request.POST.get('CallDuration', 0)

        Call.objects.filter(call_sid=call_sid).update(
            status=call_status,
            duration=int(duration) if duration else None,
        )

        return HttpResponse(status=204)
