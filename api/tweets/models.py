import logging
logger = logging.getLogger(__name__)

from datetime import datetime

from django.db import models
from django.db.utils import IntegrityError

from behaviors.models import Timestampable

from tweets.utilities import get_tweet_id

class Tweet(Timestampable):
    twitter_id = models.TextField(null=False, unique=True)
    favorite_count = models.IntegerField(null=True)
    user_handle = models.TextField(null=False)
    user_name = models.TextField(null=True)
    text = models.TextField(null=False)
    truncated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(null=True)

    @staticmethod
    def create_from_tweet(tweet):
        twitter_id = get_tweet_id(tweet)
        favorite_count = int(tweet.get('favourite_count', 0))
        user_handle = tweet.get('from_user_name', 'HANDLE MISSING')
        user_name = tweet.get('from_user_realname', 'REAL NAME NOT SET')
        text = tweet.get('text', 'TWEET MISSING')
        truncated = not (tweet.get('truncated', '') == '')
        timestamp = datetime.fromisoformat(tweet.get('created_at'))

        try:
            Tweet(
                twitter_id=twitter_id,
                favorite_count=favorite_count,
                user_handle=user_handle,
                user_name=user_name,
                text=text,
                truncated=truncated,
                timestamp=timestamp
            ).save()
        except IntegrityError as error:
            logger.info(f'Tweet with id {twitter_id} already exists. Here is the error:\t{error}')



class Url(Timestampable):
    short_url = models.URLField(null=False)
    resolved_url = models.URLField(null=True)
    domain = models.TextField(null=True)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE)
