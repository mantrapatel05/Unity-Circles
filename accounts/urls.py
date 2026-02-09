from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, StudentProfileView, UserListView, current_user

router = DefaultRouter()
router.register(r'register', UserRegistrationView, basename='user-register')
router.register(r'profile', StudentProfileView, basename='student-profile')
router.register(r'users', UserListView, basename='user-list')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', current_user, name='current_user'),
]