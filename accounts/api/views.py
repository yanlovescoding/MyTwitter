from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import logout as django_logout
from accounts.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.queryset.get(id=4)
    #     serializer = self.get_serializer(instance)
    #     print("xxxxxxxx")
    #     User.objects.create(username="abc100", email="efg1@test.com", password="abcdefg")
    #
    #     return Response(serializer.data)


class AccountViewSet(viewsets.ViewSet):
    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)


    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({'Logout Success': True})
