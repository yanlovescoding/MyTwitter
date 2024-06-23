from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from likes.models import Like
from rest_framework.decorators import action
from likes.api.serializers import (
    LikeSerializer,
    LikeSerializerForCreate,
)



class LikeViewSet(viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializerForCreate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = LikeSerializerForCreate(
            data=request.data,
            context={'request': request},
        )
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        like = serializer.save()
        return Response(
            LikeSerializer(like).data,
            status=201,
        )

    def list(self, request, *args, **kwargs):
        return Response(
            {'message': 'This is like data'})