from django.contrib import admin
from django.urls import path, include
from accounts.api import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
