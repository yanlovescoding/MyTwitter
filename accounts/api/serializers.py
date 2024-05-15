from rest_framework import serializers,exceptions
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=2)
    password = serializers.CharField(max_length=20, min_length=5)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password','email']

    def validate(self, data):
        if User.objects.filter(username = data['username'].lower()).exists():
            raise exceptions.ValidationError({
                'message':'This user name has been occupied.'
            })
        if User.objects.filter(username = data['email'].lower()).exists():
            raise exceptions.ValidationError({
                'message':'This email has been occupied.'
            })
        return data

    def create(self, validated_data):
        username = validated_data['username'].lower()
        password = validated_data['password']
        email = validated_data['email'].lower()

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        return user






# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     class Meta:
#         model = User
#         fields = User
