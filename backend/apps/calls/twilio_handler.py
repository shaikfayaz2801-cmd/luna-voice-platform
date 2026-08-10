"""
Twilio integration handler — TwiML generation and webhook processing.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def generate_twiml_connect(call_sid: str) -> str:
    """
    Generate TwiML to connect a Twilio call to our Media Stream WebSocket.
    Returns XML string for Twilio webhook response.
    """
    ws_url = f"{settings.TWILIO_WEBHOOK_URL.replace('https://', 'wss://').replace('http://', 'ws://')}/ws/calls/{call_sid}/"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">Please hold on, connecting you to Luna.</Say>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>"""


def generate_twiml_say(message: str, voice: str = 'alice') -> str:
    """Generate simple TwiML Say response."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{voice}">{message}</Say>
</Response>"""


def generate_twiml_outbound(to: str, from_: str, call_sid: str) -> str:
    """TwiML for initiating an outbound call and connecting to media stream."""
    ws_url = f"{settings.TWILIO_WEBHOOK_URL.replace('https://', 'wss://')}/ws/calls/{call_sid}/"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="{ws_url}" />
    </Connect>
</Response>"""


def initiate_outbound_call(to: str, user) -> dict:
    """
    Initiate an outbound Twilio call.
    Returns dict with call_sid or error.
    """
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        call = client.calls.create(
            to=to,
            from_=settings.TWILIO_PHONE_NUMBER,
            url=f"{settings.TWILIO_WEBHOOK_URL}/api/calls/webhook/",
            status_callback=f"{settings.TWILIO_WEBHOOK_URL}/api/calls/status-callback/",
            status_callback_method='POST',
        )
        return {'call_sid': call.sid, 'status': call.status}
    except Exception as e:
        logger.exception(f"Outbound call error: {e}")
        return {'error': str(e)}
