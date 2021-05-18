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
from slovenian_time import get_cet_time_from_twint_datestring

logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))

# TODO remove dmi_tcat dependency
# and instead take tweets from the DB
# @shared_task
# def resolve_urls_for_date(date):
#     tweets = fetch_tweets_for_date_string(date)

#     for tweet in tweets:
#         logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
#         resolve_url_for_tweet.delay(tweet)


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
def store_all_tweets():
    # no data exists before 2020-08-24
    tweets_start_date = date(2020, 8, 24)
    today = date.today()
    delta = today - tweets_start_date

    start, end = get_summary_date_range(days=delta.days)
    tweets = fetch_tweets_for_date_string(start, end)

    store_tweets(tweets).delay()

@shared_task
def refresh_tweets_on_date(date):
    if not is_valid_date_string(date):
        raise ValueError(f'The provided date ({date}) could not be parsed.')

    tweets = []

    twint_config = twint.Config()
    twint_config.Hide_output = True
    twint_config.Store_object = True
    twint_config.Store_object_tweets_list = tweets
    twint_config.Username = "jjansasds"
    twint_config.Since = date
    twint_config.Until = tomorrow(date)

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
