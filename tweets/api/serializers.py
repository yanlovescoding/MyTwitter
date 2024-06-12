from rest_framework import serializers,exceptions
from django.contrib.auth.models import User
from tweets.models import Tweet
from accounts.api.serializers import (
    UserSerializer,
)
from comments.api.serializers import (
    CommentSerializer,
)

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')

class TweetSerializerWithComment(TweetSerializer):
    user = UserSerializer()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content', 'comments')

class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet