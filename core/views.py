from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Community, Post, PostComment, Meeting
from .serializers import CommunitySerializer, PostSerializer, PostCommentSerializer, MeetingSerializer
from .forms import CreateCommunityForm

ALLOWED_PAGES = [
    'landing',
    'login',
    'dashboard',
    'signup',
    'communities',
    'mentors',
    'meetings',
    'messages',
    'profile',
    'onboarding',
]

def page(request, page_name):
    if page_name not in ALLOWED_PAGES:
        raise Http404()
    return render(request, f'{page_name}.html')


def communities_view(request):
    communities = Community.objects.all()
    return render(request, "communities.html", {
        "communities": communities
    })


@login_required
def create_community(request):
    if request.method == "POST":
        form = CreateCommunityForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            community.members.add(request.user)
            return redirect("communities")
    else:
        form = CreateCommunityForm()

    return render(request, "create_community.html", {"form": form})


@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == "POST":
        if request.user not in community.members.all():
            community.members.add(request.user)
    return redirect("communities")


@login_required
def leave_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == "POST":
        if request.user in community.members.all():
            community.members.remove(request.user)
    return redirect("communities")


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        community = self.get_object()
        if request.user not in community.members.all():
            community.members.add(request.user)
        return Response({'status': 'joined'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        community = self.get_object()
        if request.user in community.members.all():
            community.members.remove(request.user)
        return Response({'status': 'left'})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        community_id = self.request.query_params.get('community_id', None)
        if community_id:
            return Post.objects.filter(community_id=community_id)
        return Post.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        post = self.get_object()
        post.upvotes += 1
        post.save()
        return Response({'upvotes': post.upvotes})
    
    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        post = self.get_object()
        post.downvotes += 1
        post.save()
        return Response({'downvotes': post.downvotes})


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        if post_id:
            return PostComment.objects.filter(post_id=post_id)
        return PostComment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        comment = self.get_object()
        comment.upvotes += 1
        comment.save()
        return Response({'upvotes': comment.upvotes})


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Meeting.objects.filter(mentor=self.request.user) | Meeting.objects.filter(attendees=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(mentor=self.request.user)
    
    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        meeting = self.get_object()
        if request.user not in meeting.attendees.all():
            meeting.attendees.add(request.user)
        return Response({'status': 'joined'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        meeting = self.get_object()
        if request.user in meeting.attendees.all():
            meeting.attendees.remove(request.user)
        return Response({'status': 'left'})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        meeting = self.get_object()
        if meeting.mentor != request.user:
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        meeting.status = 'cancelled'
        meeting.save()
        return Response({'status': 'cancelled'})
