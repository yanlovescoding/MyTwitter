from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     class Meta:
#         model = User
#         fields = User
