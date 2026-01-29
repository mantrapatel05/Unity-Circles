from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MentorshipRequest, Mentorship
from .serializers import MentorshipRequestSerializer, MentorshipSerializer


class MentorshipRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MentorshipRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MentorshipRequest.objects.filter(student=self.request.user) | MentorshipRequest.objects.filter(mentor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        mentorship_request = self.get_object()
        if mentorship_request.mentor != request.user:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        mentorship_request.status = 'accepted'
        mentorship_request.save()
        Mentorship.objects.create(request=mentorship_request)
        
        return Response({'status': 'Mentorship accepted'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        mentorship_request = self.get_object()
        if mentorship_request.mentor != request.user:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        mentorship_request.status = 'rejected'
        mentorship_request.save()
        
        return Response({'status': 'Mentorship rejected'})


class MentorshipViewSet(viewsets.ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    permission_classes = [IsAuthenticated]
