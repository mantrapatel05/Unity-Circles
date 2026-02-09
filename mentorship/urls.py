from django.urls import path
from .views import mentors_view, register_mentor

urlpatterns = [
    path('', mentors_view, name='mentors'),
    path('register/', register_mentor, name='register_mentor'),
]
