from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import OnboardingStep
from .serializers import OnboardingStepSerializer


class OnboardingStepViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingStepSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return OnboardingStep.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete_profile(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.profile_completed = True
        onboarding.check_completion()
        return Response({'status': 'Profile step completed'})
    
    @action(detail=True, methods=['post'])
    def complete_interests(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.interests_completed = True
        onboarding.check_completion()
        return Response({'status': 'Interests step completed'})
    
    @action(detail=True, methods=['post'])
    def complete_goals(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.goals_completed = True
        onboarding.check_completion()
        return Response({'status': 'Goals step completed'})
    
    @action(detail=True, methods=['post'])
    def complete_community(self, request, pk=None):
        onboarding = self.get_object()
        onboarding.community_completed = True
        onboarding.check_completion()
        return Response({'status': 'Community step completed'})
