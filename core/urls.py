from django.urls import path
from .views import page, communities_view, create_community, join_community, leave_community

urlpatterns = [
    path('', page, {'page_name': 'landing'}, name='landing'),
    path('login/', page, {'page_name': 'login'}, name='login'),
    path('signup/', page, {'page_name': 'signup'}, name='signup'),
    
    # Communities
    path('communities/', communities_view, name='communities'),
    path('communities/create/', create_community, name='create_community'),
    path('communities/join/<int:community_id>/', join_community, name='join_community'),
    path('communities/leave/<int:community_id>/', leave_community, name='leave_community'),
    
    # Generic page routing (MUST BE LAST)
    path('<str:page_name>/', page),
]
