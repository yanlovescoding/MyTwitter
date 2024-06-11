from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from tweets.models import Tweet
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate,
    CommentSerializerForUpdate,
)
from tweets.api.serializers import (
    TweetSerializer,
)


class CommentViewSet(viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    filterset_fields = ('tweet_id',)
    serializer_class = CommentSerializerForUpdate

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    # api/comments/?tweet_id=8 => list out all comments under then tweet_id 8
    def list(self, request, *args, **kwargs):
        if 'tweet_id' not in request.query_params:
            return Response(
                {
                    'message': 'missing tweet_id in request',
                    'success': False,
                },
                status=400,
            )
        queryset = self.get_queryset()
        comments = self.filter_queryset(queryset).order_by('created_at')
        print(comments.count())
        serializer = CommentSerializer(comments, many=True)
        return Response(
            {'comments': serializer.data},
            status=200
        )

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

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.delete()
        return Response({'success': True}, status=200)