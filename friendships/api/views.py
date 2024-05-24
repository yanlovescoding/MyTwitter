from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from friendships.models import Friendships
from friendships.api.serializers import (
    FollowSerializer,
)


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer()

    @action(methods=['GET'], detail=True, permission_classes=[AllowAny])
    def followers(self, request, pk):
        # GET /api/friendships/pk/followers/ , as a current user, A is following pk, I would like to check user pk have how many followers
        friendships = Friendships.objects.filter(to_user_id=pk).order_by('-created_at')
        serializer = FollowSerializer(friendships, many=True)
        return Response(
            {'followers': serializer.data},
            status=200,
        )

    def list(self, request, *args, **kwargs):
        return Response(
            {'message': 'This is friendship data'})

