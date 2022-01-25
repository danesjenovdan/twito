import os
from datetime import date, datetime

from celery import Celery, shared_task

from django.apps import apps
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
apps.populate(settings.INSTALLED_APPS)

from tweets.utilities import get_tweet_id, get_summary_date_range
from tweets.models import Tweet

from url_resolver import get_urls_from_tweet
from settings import CELERY_CONFIG
import logging

import twint
from utils import is_valid_date_string, tomorrow, full_tweet_text
from slovenian_time import get_cet_time_from_twint_datestring, now

logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))

celery.conf.beat_schedule = {
    'refresh-tweets-every-15-minutes': {
        'task': 'tasks.refresh_tweets',
        'schedule': 60.0 * 15.0
    },
}
celery.conf.timezone = 'CET'


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def resolve_url_for_tweet(tweet):

    logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
    result = get_urls_from_tweet(tweet)

    # store url(s)
    if result:
        logger.info(result)

@shared_task
def store_tweets(tweets):
    for tweet in tweets:
        Tweet.create_from_tweet(tweet)
        # resolve url for tweet
        # logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
        # resolve_url_for_tweet.delay(tweet)

@shared_task
def refresh_tweets_on_date_string(date_string):
    if not is_valid_date_string(date_string):
        raise ValueError(f'The provided date ({date_string}) could not be parsed.')

    tweets = []

    twint_config = twint.Config()
    twint_config.Hide_output = True
    twint_config.Store_object = True
    twint_config.Store_object_tweets_list = tweets
    twint_config.Username = "jjansasds"
    twint_config.Since = date_string
    twint_config.Until = tomorrow(date_string)

    # Run
    # twint.run.Profile(twint_config)
    twint.run.Profile(twint_config)
    
    for tweet in tweets:
        db_tweet, created = Tweet.objects.get_or_create(twitter_id=tweet.id_str)

        db_tweet.user_handle = tweet.username
        db_tweet.timestamp = get_cet_time_from_twint_datestring(tweet.datetime)
        db_tweet.text = full_tweet_text(tweet)

        db_tweet.retweet = bool(tweet.retweet)
        if db_tweet.retweet:
            db_tweet.retweet_timestamp = get_cet_time_from_twint_datestring(tweet.retweet_date)
            db_tweet.retweet_id = tweet.retweet_id
            db_tweet.retweet_quote = bool(tweet.quote_url)
            if bool(tweet.quote_url):
                db_tweet.retweet_quote_url = tweet.quote_url
        
        db_tweet.quote = bool(tweet.quote_url)
        if db_tweet.quote:
            db_tweet.quote_url = tweet.quote_url
        
        db_tweet.favorite_count = int(tweet.likes_count)
        db_tweet.retweet_count = int(tweet.retweets_count)

        db_tweet.save()

@shared_task
def refresh_tweets():
    now_string = now().strftime('%Y-%m-%d')
    logger.info(f'START Fetching tweets for {now_string} ...')
    refresh_tweets_on_date_string(now_string)
    logger.info(f'END Fetching tweets for {now_string} ...')
