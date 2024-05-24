from django.contrib import admin
from friendships.models import Friendships

# Register your models here.
@admin.register(Friendships)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id','from_user', 'to_user', 'created_at')
    date_hierarchy = 'created_at'