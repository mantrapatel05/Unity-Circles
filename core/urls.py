from django.urls import path
from .views import page

urlpatterns = [
    path('', page, {'page_name': 'landing'}, name='landing'),
    path('login/', page, {'page_name': 'login'}, name='login'),
    path('signup/', page, {'page_name': 'signup'}, name='signup'),
    path('<str:page_name>/', page),
]
