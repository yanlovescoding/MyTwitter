from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from tweets.models import Tweet
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from tweets.api.serializers import (
    TweetSerializer,
)


class CommentViewSet(viewsets.GenericViewSet):
    queryset = Tweet.objects.all()
    serializer_class = CommentSerializerForUpdate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request):
        data = {
            'user_id': request.user.id,
            'tweet_id': request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        return Response(
            CommentSerializer(tweet).data,
            status=201,
        )
    def update(self, request, *args, **kwargs):
        serializer = CommentSerializerForUpdate(
            instance=self.get_object(),
            data=request.data,
        )
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=400)
        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=200,
        )

    def list(self, request, *args, **kwargs):
        tweets = Tweet.objects.filter(
            user_id=request.user.id
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response(
            {'tweets': serializer.data},
            status=200
        )
