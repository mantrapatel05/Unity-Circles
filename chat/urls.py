from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    messages_page, 
    send_message, 
    DirectMessageViewSet,
    send_message_api,
    get_users,
    get_all_users_for_new_chat
)

router = DefaultRouter()
router.register(r'messages', DirectMessageViewSet, basename='directmessage')

urlpatterns = [
    # Web views
    path("", messages_page, name="messages"),
    path("send/", send_message, name="send_message"),
    
    # API endpoints
    path("api/", include(router.urls)),
    path("api/send/", send_message_api, name="send_message_api"),
    path("api/users/", get_users, name="get_users"),
    path("api/all-users/", get_all_users_for_new_chat, name="get_all_users_for_new_chat"),
]
