from rest_framework import serializers,exceptions
from django.contrib.auth.models import User
from comments.models import Comment
from tweets.models import Tweet
from tweets.api.serializers import (
    TweetSerializer,
)
from accounts.api.serializers import (
    UserSerializer,
)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ('user', 'tweet', 'content', 'created_at', 'updated_at')

class CommentSerializerForCreate(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    class Meta:
        model = Tweet
        fields = ('content', 'tweet_id','user_id')

    def validate(self, data):
        tweet_id = data['tweet_id']
        if not Tweet.objects.filter(id=tweet_id).exists():
            raise exceptions.ValidationError({
                'message': 'Tweet does not exist'
            })
        return data
    def create(self, validated_data):
        user_id = validated_data['user_id']
        content = validated_data['content']
        tweet_id = validated_data['tweet_id']
        return Comment.objects.create(
            user_id=user_id,
            tweet_id=tweet_id,
            content=content
        )
