from rest_framework import serializers,exceptions
from django.contrib.auth.models import User
from newsfeeds.models import NewsFeed
from tweets.models import Tweet
from tweets.api.serializers import (
    TweetSerializer,
)

class NewfeedsSerializer(serializers.ModelSerializer):
    # user = TweetSerializer()
    class Meta:
        model = NewsFeed
        fields = ( 'id','tweet', 'created_at')