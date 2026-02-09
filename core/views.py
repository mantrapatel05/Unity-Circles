from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import StudentProfile
from core.models import Community, Post, PostComment, Meeting
from core.serializers import MeetingSerializer, UserMinimalSerializer

ALLOWED_PAGES = [
    'landing',
    'login',
    'signup',
    'dashboard',
    'communities',
    'meetings',
]

def page(request, page_name):
    if page_name not in ALLOWED_PAGES:
        raise Http404()
    return render(request, f"{page_name}.html")

# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # Create student profile
        StudentProfile.objects.create(user=user)
        
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('/dashboard/')
    
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')

# Profile View
@login_required
def profile_view(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile
        profile.bio = request.POST.get('bio', '')
        profile.role = request.POST.get('role', '')
        profile.interests = request.POST.get('interests', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('/profile/')
    
    return render(request, 'profile.html', {'profile': profile})

# Dashboard View
@login_required
def dashboard_view(request):
    from mentorship.models import MentorProfile
    from chat.models import DirectMessage
    
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    my_communities = Community.objects.filter(members=request.user)
    recent_posts = Post.objects.filter(community__in=my_communities).order_by('-created_at')[:5]
    
    # Get stats
    mentors_count = MentorProfile.objects.count()
    communities_count = my_communities.count()
    messages_count = DirectMessage.objects.filter(receiver=request.user).count()
    
    from django.db.models import Q
    meetings_count = Meeting.objects.filter(
        Q(mentor=request.user) | Q(attendees=request.user)
    ).filter(status='scheduled').count()
    
    # Get recommended mentors
    recommended_mentors = User.objects.filter(mentor_profile__isnull=False)[:3]
    
    return render(request, 'dashboard.html', {
        'profile': profile,
        'my_communities': my_communities,
        'recent_posts': recent_posts,
        'stats': {
            'mentors_count': mentors_count,
            'communities_count': communities_count,
            'messages_count': messages_count,
            'meetings_count': meetings_count,
        },
        'recommended_mentors': recommended_mentors,
    })

# Communities Views
@login_required
def communities_view(request):
    communities = Community.objects.all().order_by('-created_at')
    my_communities = Community.objects.filter(members=request.user)
    
    return render(request, 'communities.html', {
        'communities': communities,
        'my_communities': my_communities,
    })

@login_required
def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    posts = Post.objects.filter(community=community).order_by('-created_at')
    is_member = community.members.filter(id=request.user.id).exists()
    
    return render(request, 'community_detail.html', {
        'community': community,
        'posts': posts,
        'is_member': is_member,
    })

@login_required
def create_community(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category', 'other')
        image = request.FILES.get('image')  # Handle image upload
        
        if name:
            community = Community.objects.create(
                name=name,
                description=description,
                category=category,
                creator=request.user,
                image=image
            )
            community.members.add(request.user)
            messages.success(request, f'Community "{name}" created successfully!')
            return redirect(f'/communities/{community.id}/')
        else:
            messages.error(request, 'Community name is required.')
    
    return render(request, 'create_community.html')

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.add(request.user)
    messages.success(request, f'You joined "{community.name}"!')
    
    # Check if request came from dashboard or elsewhere
    next_url = request.GET.get('next', f'/communities/{community.id}/')
    return redirect(next_url)

@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    community.members.remove(request.user)
    messages.success(request, f'You left "{community.name}".')
    return redirect('/communities/')

# Post Views
@login_required
def create_post(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    
    if not community.members.filter(id=request.user.id).exists():
        messages.error(request, 'You must be a member to post.')
        return redirect(f'/communities/{community_id}/')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Handle image upload
        
        if title and content:
            post = Post.objects.create(
                community=community,
                author=request.user,
                title=title,
                content=content,
                image=image
            )
            messages.success(request, 'Post created successfully!')
            return redirect(f'/communities/{community_id}/')
        else:
            messages.error(request, 'Title and content are required.')
    
    return render(request, 'create_post.html', {'community': community})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = PostComment.objects.filter(post=post).order_by('created_at')
    
    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
    })

@login_required
def upvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes += 1
    post.save()
    messages.success(request, 'Post upvoted!')
    return redirect(f'/posts/{post_id}/')

@login_required
def downvote_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.downvotes += 1
    post.save()
    messages.success(request, 'Post downvoted.')
    return redirect(f'/posts/{post_id}/')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content:
            PostComment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Comment added!')
        else:
            messages.error(request, 'Comment cannot be empty.')
    
    return redirect(f'/posts/{post_id}/')


# Simple Meeting Views (No API)
@login_required
def meetings_view(request):
    """Simple meetings page - shows all user's meetings"""
    from django.db.models import Q
    
    # Get meetings where user is mentor or attendee
    my_meetings = Meeting.objects.filter(
        Q(mentor=request.user) | Q(attendees=request.user)
    ).distinct().order_by('-scheduled_time')
    
    return render(request, 'meetings_simple.html', {
        'meetings': my_meetings
    })


@login_required
def create_meeting(request, community_id):
    """Create a meeting for a community - simple form POST"""
    community = get_object_or_404(Community, id=community_id)
    
    if not community.members.filter(id=request.user.id).exists():
        messages.error(request, 'You must be a member to create meetings.')
        return redirect(f'/communities/{community_id}/')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        date = request.POST.get('date')
        time = request.POST.get('time')
        duration = request.POST.get('duration', 60)
        zoom_link = request.POST.get('zoom_link', '')
        
        if title and date and time:
            # Combine date and time
            from datetime import datetime
            scheduled_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
            
            meeting = Meeting.objects.create(
                title=title,
                description=description,
                mentor=request.user,
                community=community,
                scheduled_time=scheduled_time,
                duration_minutes=int(duration),
                zoom_link=zoom_link if zoom_link else None,
                status='scheduled'
            )
            messages.success(request, f'Meeting "{title}" scheduled successfully!')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return redirect(f'/communities/{community_id}/')


@login_required
def join_meeting(request, meeting_id):
    """Join a meeting as an attendee"""
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.attendees.add(request.user)
    messages.success(request, f'You joined "{meeting.title}"!')
    return redirect('/meetings/')


@login_required
def leave_meeting(request, meeting_id):
    """Leave a meeting"""
    meeting = get_object_or_404(Meeting, id=meeting_id)
    meeting.attendees.remove(request.user)
    messages.success(request, f'You left "{meeting.title}".')
    return redirect('/meetings/')


# Meeting API ViewSet
class MeetingViewSet(viewsets.ModelViewSet):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get meetings where user is mentor or attendee"""
        from django.db.models import Q
        return Meeting.objects.filter(
            Q(mentor=self.request.user) | Q(attendees=self.request.user)
        ).distinct().order_by('-scheduled_time')

    def perform_create(self, serializer):
        """Automatically set the mentor to the current user"""
        community_id = self.request.data.get('community_id')
        community = None
        if community_id:
            community = get_object_or_404(Community, id=community_id)
        
        meeting = serializer.save(mentor=self.request.user, community=community)
        # Add selected attendees
        attendees_ids = self.request.data.get('attendees', [])
        if attendees_ids:
            meeting.attendees.set(attendees_ids)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a meeting"""
        meeting = self.get_object()
        meeting.attendees.add(request.user)
        return Response({'status': 'joined'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a meeting"""
        meeting = self.get_object()
        meeting.attendees.remove(request.user)
        return Response({'status': 'left'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_for_meeting(request):
    """Get list of all users for meeting invites"""
    users = User.objects.exclude(id=request.user.id).order_by('username')
    serializer = UserMinimalSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_community_meetings(request, community_id):
    """Get meetings for a specific community"""
    community = get_object_or_404(Community, id=community_id)
    
    # Check if user is a member
    if not community.members.filter(id=request.user.id).exists():
        return Response({'error': 'You must be a member to view meetings'}, status=status.HTTP_403_FORBIDDEN)
    
    meetings = Meeting.objects.filter(community=community).order_by('-scheduled_time')
    serializer = MeetingSerializer(meetings, many=True)
    return Response(serializer.data)
