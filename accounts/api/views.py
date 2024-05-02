from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from accounts.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
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



