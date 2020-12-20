from celery import Celery
from dmi_tcat import fetch_tweets_for_date
from url_resolver import get_urls_from_tweet
from config import CELERY_CONFIG

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))


@celery.task
def resolve_urls_for_date(date):
    tweets = fetch_tweets_for_date(date)

    for tweet in tweets:
        resolve_url_for_tweet.delay(tweet)


@celery.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def resolve_url_for_tweet(tweet):
    result = get_urls_from_tweet([tweet])

