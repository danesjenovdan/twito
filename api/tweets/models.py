import logging
logger = logging.getLogger(__name__)

from datetime import datetime

from django.db import models
from django.db.utils import IntegrityError

from behaviors.models import Timestampable

class Tweet(Timestampable):
    twitter_id = models.TextField(null=False, unique=True)
    timestamp = models.DateTimeField(null=True)
    text = models.TextField(null=False)

    retweet = models.BooleanField(default=False)
    retweet_timestamp = models.DateTimeField(null=True)
    retweet_id = models.TextField(null=True)
    retweet_quote = models.BooleanField(default=False)
    retweet_quote_url = models.URLField(null=True)

    quote = models.BooleanField(default=False)
    quote_url = models.URLField(null=True)

    favorite_count = models.IntegerField(null=True)
    retweet_count = models.IntegerField(null=True)

    user_handle = models.TextField(null=False)


class Url(Timestampable):
    short_url = models.URLField(null=False)
    resolved_url = models.URLField(null=True)
    domain = models.TextField(null=True)
    tweet = models.ForeignKey('tweets.Tweet', on_delete=models.CASCADE)


class DailySummary(models.Model):
    date = models.DateField()
    time = models.IntegerField(null=True)
