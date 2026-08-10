from django.urls import path
from .views import CallListView, InitiateCallView, TwilioWebhookView, TwilioStatusCallbackView

urlpatterns = [
    path('', CallListView.as_view(), name='call-list'),
    path('initiate/', InitiateCallView.as_view(), name='initiate-call'),
    path('webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),
    path('status-callback/', TwilioStatusCallbackView.as_view(), name='twilio-status'),
]
