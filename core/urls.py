from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import (
    page, login_view, signup_view, logout_view,
    profile_view, dashboard_view, communities_view,
    community_detail, create_community, join_community, leave_community,
    create_post, post_detail, upvote_post, downvote_post, add_comment,
    meetings_view, create_meeting, join_meeting, leave_meeting,
    MeetingViewSet, get_users_for_meeting, get_community_meetings
)

# API Router
router = DefaultRouter()
router.register(r'meetings', MeetingViewSet, basename='meeting')

urlpatterns = [
    # Authentication
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    
    # Profile
    path('profile/', profile_view, name='profile'),
    
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Communities
    path('communities/', communities_view, name='communities'),
    path('communities/<int:community_id>/', community_detail, name='community_detail'),
    path('communities/create/', create_community, name='create_community'),
    path('communities/<int:community_id>/join/', join_community, name='join_community'),
    path('communities/<int:community_id>/leave/', leave_community, name='leave_community'),
    
    # Posts
    path('communities/<int:community_id>/post/', create_post, name='create_post'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('posts/<int:post_id>/upvote/', upvote_post, name='upvote_post'),
    path('posts/<int:post_id>/downvote/', downvote_post, name='downvote_post'),
    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    
    # Meetings - Simple (No API)
    path('meetings/', meetings_view, name='meetings'),
    path('communities/<int:community_id>/meeting/', create_meeting, name='create_meeting'),
    path('meetings/<int:meeting_id>/join/', join_meeting, name='join_meeting'),
    path('meetings/<int:meeting_id>/leave/', leave_meeting, name='leave_meeting'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/auth/users/', get_users_for_meeting, name='get_users_for_meeting'),
    path('api/communities/<int:community_id>/meetings/', get_community_meetings, name='get_community_meetings'),
    
    # Landing
    path('', page, {'page_name': 'landing'}, name='landing'),
    
    # Catch-all (MUST BE LAST)
    path('<str:page_name>/', page),
]
