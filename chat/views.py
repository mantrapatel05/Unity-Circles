from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import DirectMessage
from .serializers import DirectMessageSerializer, UserMinimalSerializer

@login_required
def messages_page(request):
    to_id = request.GET.get("to")
    chat_user = None
    messages = []

    if to_id:
        chat_user = get_object_or_404(User, id=to_id)
        messages = DirectMessage.objects.filter(
            Q(sender=request.user, receiver=chat_user) |
            Q(sender=chat_user, receiver=request.user)
        ).order_by("created_at")

    # Get only users with whom current user has conversations (privacy fix)
    users_with_conversations = User.objects.filter(
        Q(dm_sent__receiver=request.user) | Q(dm_received__sender=request.user)
    ).distinct().order_by('username')

    return render(request, "messages.html", {
        "chat_user": chat_user,
        "messages": messages,
        "mentors": users_with_conversations,  # Only users with existing conversations
    })


@login_required
def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get("receiver")
        content = request.POST.get("content")

        if receiver_id and content:
            DirectMessage.objects.create(
                sender=request.user,
                receiver_id=receiver_id,
                content=content
            )

        return redirect(f"/chat/?to={receiver_id}")
    return redirect("/chat/")


# API Views
class DirectMessageViewSet(viewsets.ModelViewSet):
    serializer_class = DirectMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get all messages for the current user"""
        return DirectMessage.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """Automatically set the sender to the current user"""
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Get list of users with whom current user has conversations"""
        user = request.user
        
        # Get all users who have sent or received messages from current user
        message_users = User.objects.filter(
            Q(dm_sent__receiver=user) | Q(dm_received__sender=user)
        ).distinct()
        
        serializer = UserMinimalSerializer(message_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def with_user(self, request):
        """Get conversation with a specific user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        messages = DirectMessage.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).order_by('created_at')
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_api(request):
    """API endpoint to send a message"""
    receiver_id = request.data.get('receiver_id')
    content = request.data.get('content')
    
    if not receiver_id or not content:
        return Response(
            {'error': 'receiver_id and content are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'Receiver not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    message = DirectMessage.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )
    
    serializer = DirectMessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    """Get list of all users except the current user"""
    users = User.objects.exclude(id=request.user.id)
    serializer = UserMinimalSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users_for_new_chat(request):
    """Get list of all users for starting new conversations"""
    users = User.objects.exclude(id=request.user.id).order_by('username')
    serializer = UserMinimalSerializer(users, many=True)
    return Response(serializer.data)
