from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet


class NewsFeed(models.Model):
    # user is the user who is following some people, user == from_user
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.CharField(Tweet, max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ((
            'user','created_at'),
        )
        unique_together = ((
            'user', 'tweet'),
        )
        ordering = (
            'user', 'created_at'
        )

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'


