from django.urls import path
from .views import PersonalityListView
urlpatterns = [path('', PersonalityListView.as_view(), name='personality-list')]
