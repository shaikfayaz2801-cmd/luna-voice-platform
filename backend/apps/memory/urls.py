from django.urls import path
from .views import MemoryListCreateView, MemoryDetailView, MemorySearchView

urlpatterns = [
    path('', MemoryListCreateView.as_view(), name='memory-list'),
    path('<uuid:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
    path('search/', MemorySearchView.as_view(), name='memory-search'),
]
