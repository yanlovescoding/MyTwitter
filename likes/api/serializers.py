from rest_framework import serializers,exceptions
from django.contrib.auth.models import User
from likes.models import Like
from tweets.models import Tweet
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from accounts.api.serializers import (
    UserSerializer,
)

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Like
        fields = ('user', 'created_at')

class LikeSerializerForCreate(serializers.ModelSerializer):
    content_type = serializers.ChoiceField(choices=['comment', 'tweet'])
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('content_type','object_id','created_at','user')

    def _get_model_class(self, data):
        if data['content_type'] == 'comment':
            return Comment
        if data['content_type'] == 'tweet':
            return Tweet
        return None
    def create(self, validated_data):
        model_class = self._get_model_class(validated_data)
        user = self.context['request'].user
        content_type = ContentType.objects.get_for_model(model_class)
        object_id = validated_data['object_id']
        instance, _= Like.objects.get_or_create(
            user=user,
            content_type=content_type,
            object_id = object_id,
        )
        return instance