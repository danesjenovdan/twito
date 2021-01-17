from datetime import date

from celery import Celery

from datetime import datetime

from tweets.utilities import get_tweet_id, get_summary_date_range
from tweets.models import Tweet

from dmi_tcat import fetch_tweets_for_date_string
from url_resolver import get_urls_from_tweet
from settings import CELERY_CONFIG
import logging

logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))


@celery.task
def resolve_urls_for_date(date):
    tweets = fetch_tweets_for_date_string(date)

    for tweet in tweets:
        logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
        resolve_url_for_tweet.delay(tweet)


@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def resolve_url_for_tweet(tweet):

    logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
    result = get_urls_from_tweet(tweet)

    # store url(s)
    if result:
        logger.info(result)

def store_tweets(tweets):
    for tweet in tweets:
        Tweet.create_from_tweet(tweet)
        # resolve url for tweet
        # logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
        # resolve_url_for_tweet.delay(tweet)

def store_all_tweets():
    # no data exists before 2020-08-24
    tweets_start_date = date(2020, 8, 24)
    today = date.today()
    delta = today - tweets_start_date

    start, end = get_summary_date_range(days=delta.days)
    tweets = fetch_tweets_for_date_string(start, end)

    store_tweets(tweets)
