from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Community
from .serializers import CommunitySerializer
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
