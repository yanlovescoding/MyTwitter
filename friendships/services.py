from friendships.models import Friendships


class FriendshipService(object):

    @classmethod
    def get_followers(cls, user):
        friendships = Friendships.objects.filter(
            to_user=user,
        ).prefetch_related('from_user')
        # print(
        #     Friendships.objects.filter(
        #     to_user=user,
        #     ).prefetch_related('from_user').
        #     query
        # )
        return [friendship.from_user for friendship in friendships]
