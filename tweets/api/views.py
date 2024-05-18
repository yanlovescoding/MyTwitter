from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from tweets.models import Tweet
from django.contrib.auth import (
    logout as django_logout,
    login as django_login,
    authenticate as django_authenticate,
)
from tweets.api.serializers import (
    TweetSerializer,
)


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    def list(self, request):
        if 'user_id' not in request.query_params:
            return Response(
                "The user is not existed",
                status=400
            )
        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response(
            {'tweets': serializer.data},
            status=200
        )

