from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Friendships(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="following_friendship_set",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="follower_friendship_set",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # For an example, A(from_user) is following B(to_user)
    # GET /api/friendships/c/followers/
    # to_user = 3, means C has 3 follower
    # from_user = 4, means C is following 4 users
    class Meta:
        index_together = (
            ('from_user_id','created_at'),
            ('to_user_id', 'created_at'),
        )
        unique_together = (
                ('from_user_id', 'to_user_id'),
        )


    def __str__(self):
        return '{} followed {}`.format(self.from_user_id, self.to_user_id)'
