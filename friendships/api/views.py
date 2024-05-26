from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from friendships.models import Friendships
from friendships.api.serializers import (
    FollowSerializer,
    FollowingSerializer,
    FriendshipSerializerForCreate,
)


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FriendshipSerializerForCreate

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        # GET /api/friendships/pk/followers/ , as a current user, A is following pk, I would like to check user pk have how many followers
        friendships = Friendships.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowSerializer(friendships, many=True)
        return Response(
            {'followers': serializer.data},
            status=200,
        )


    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followings(self, request, pk):
        # GET /api/friendships/pk/followings/ , as a current user, pk is following followers, I would like to check how many followers pk is following
        friendships = Friendships.objects.filter(from_user_id=pk).order_by('-created_at')
        serializer = FollowingSerializer(friendships, many=True)
        return Response(
            {'followings': serializer.data},
            status=200,
        )

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def follow(self, request, pk):
        if Friendships.objects.filter(from_user=request.user, to_user=pk).exists():
            return Response({
                'success': True,
                'duplicate': True,
            }, status=201)
        serializer = FriendshipSerializerForCreate(
            data={
                'from_user_id': request.user.id,
                'to_user_id': int(pk),
            }
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors,
            }, status=400)
        serializer.save()
        return Response({
            "from_user_id": request.user.id,
            'to_user_id': pk,
        },
            status=201
        )

    @action(methods=['POST'], detail=True, permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk):
        if request.user.id == int(pk):
            return Response({
                'success': False,
                'message': 'You cannot unfollow yourself',
            }, status=400)
        deleted, _ = Friendships.objects.filter(
            from_user=request.user,
            to_user=pk,
        ).delete()
        return Response({'success': True, 'deleted': deleted})

    def list(self, request, *args, **kwargs):
        return Response(
            {'message': 'This is friendship data'})

