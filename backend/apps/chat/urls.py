from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationListCreateView.as_view(), name='conversation-list'),
    path('<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('<uuid:pk>/archive/', views.ArchiveConversationView.as_view(), name='conversation-archive'),
    path('<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    path('<uuid:conversation_id>/stream/', views.StreamingMessageView.as_view(), name='message-stream'),
    path('stats/', views.ConversationStatsView.as_view(), name='conversation-stats'),
]
