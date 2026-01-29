from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MentorshipRequestViewSet, MentorshipViewSet

router = DefaultRouter()
router.register(r'requests', MentorshipRequestViewSet, basename='mentorship-request')
router.register(r'mentorships', MentorshipViewSet, basename='mentorship')

urlpatterns = [
    path('', include(router.urls)),
]
