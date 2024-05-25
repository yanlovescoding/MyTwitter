from rest_framework import serializers,exceptions
from friendships.models import Friendships
from accounts.api.serializers import UserSerializerForFriendship

class FollowSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source='from_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Friendships
        fields = ('user', 'created_at')

class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializerForFriendship(source='to_user')
    created_at = serializers.DateTimeField()

    class Meta:
        model = Friendships
        fields = ('user', 'created_at')