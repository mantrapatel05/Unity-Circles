from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OnboardingStepViewSet

router = DefaultRouter()
router.register(r'steps', OnboardingStepViewSet, basename='onboarding-step')

urlpatterns = [
    path('', include(router.urls)),
]
