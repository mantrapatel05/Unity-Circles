from django.shortcuts import render
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Community
from .serializers import CommunitySerializer

ALLOWED_PAGES = [
    'landing',
    'login',
    'dashboard',
    'signup',
    'communities',
    'mentors',
    'meetings',
    'messages',
    'profile',
    'onboarding',
]

def page(request, page_name):
    if page_name not in ALLOWED_PAGES:
        raise Http404()
    return render(request, f'{page_name}.html')


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
