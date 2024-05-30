from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import (
    NewfeedsSerializer,
)

class NewsFeedsViewSet(viewsets.ModelViewSet):
    serializer_class = NewfeedsSerializer
    def get_queryset(self):
        return NewsFeed.objects.all()
    def list(self, request, *args, **kwargs):
        serializer = NewfeedsSerializer(self.get_queryset().filter(user=request.user), many=True)
        return Response(
            {
                'news feed': serializer.data,
             }, status=200)