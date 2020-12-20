from datetime import date

from celery import Celery

from tweets import get_tweet_id, get_date_range
from dmi_tcat import fetch_tweets_for_date
from url_resolver import get_urls_from_tweet
from config import CELERY_CONFIG
import logging

logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))


@celery.task
def resolve_urls_for_date(date):
    tweets = fetch_tweets_for_date(date)

    for tweet in tweets:
        logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
        resolve_url_for_tweet.delay(tweet)


@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def resolve_url_for_tweet(tweet):
    result = get_urls_from_tweet(tweet)

    if result:
        logger.info(result)


@celery.task()
def resolve_urls_for_all_tweets():
    tweets_start_date = date(2020, 8, 24)
    today = date.today()
    delta = today - tweets_start_date

    start, end = get_date_range(delta.days)
    tweets = fetch_tweets_for_date(start, end)

    for tweet in tweets:
        logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
        resolve_url_for_tweet.delay(tweet)

