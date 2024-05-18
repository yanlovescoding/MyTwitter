from rest_framework import serializers,exceptions
from django.contrib.auth.models import User
from tweets.models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')