from django.db import models

from behaviors.models import Timestampable

class Tweet(Timestampable):
    twitter_id = models.TextField(null=False, unique=True)
    favorite_count = models.IntegerField(null=True)
    user_handle = models.TextField(null=False)
    user_name = models.TextField(null=True)
    text = models.TextField(null=False)
    truncated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True)

    def create_from_tweet(self, tweet):
        twitter_id = get_tweet_id(tweet)
        favorite_count = int(tweet.get('favourite_count', 0))
        user_handle = tweet.get('from_user_name', 'HANDLE MISSING')
        user_name = tweet.get('from_user_realname', 'REAL NAME NOT SET')
        text = tweet.get('text', 'TWEET MISSING')
        truncated = not (tweet.get('truncated', '') == '')
        time = datetime.fromisoformat(tweet.get('created_at'))

        self(
            twitter_id=twitter_id,
            favorite_count=favorite_count,
            user_handle=user_handle,
            user_name=user_name,
            text=text,
            truncated=truncated,
            time=time
        ).save()


class Url(Timestampable):
    short_url = models.URLField(null=False)
    resolved_url = models.URLField(null=True)
    domain = models.TextField(null=True)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE)
