from rest_framework import serializers,exceptions
from friendships.models import Friendships
from accounts.api.serializers import UserSerializerForFriendship
from django.contrib.auth.models import User

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

class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendships
        fields = ('from_user_id', 'to_user_id')

    def validate(self, data):
        if data['from_user_id'] == data['to_user_id']:
            raise exceptions.ValidationError({
                'message': 'from_user_id and to_user_id should be different.'
            })
        return data

    def create(self, validated_data):
        from_user_id = validated_data['from_user_id']
        to_user_id = validated_data['to_user_id']
        return Friendships.objects.create(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
        )
