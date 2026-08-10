from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Memory
from .serializers import MemorySerializer
from .retrieval import retrieve_relevant_memories

class MemoryListCreateView(generics.ListCreateAPIView):
    serializer_class = MemorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # In a real app, generate embedding here before save
        serializer.save(user=self.request.user)

class MemoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user)

class MemorySearchView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        query = request.data.get('query')
        limit = int(request.data.get('limit', 5))
        memories = retrieve_relevant_memories(request.user.id, query, limit)
        serializer = MemorySerializer(memories, many=True)
        return Response(serializer.data)
