import os
from datetime import date, datetime

from celery import Celery, shared_task

from django.apps import apps
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
apps.populate(settings.INSTALLED_APPS)

from tweets.utilities import get_tweet_id, get_summary_date_range, daily_time
from tweets.models import Tweet, Url

from url_resolver import get_urls_from_tweet, get_domain_from_url
from urllib.parse import urlparse
from settings import CELERY_CONFIG
import logging

import tweepy
from utils import is_valid_date_string, tomorrow
from slovenian_time import now, start_in_iso_utc_format, end_in_iso_utc_format


logger = logging.getLogger(__name__)

celery = Celery('tasks', broker=CELERY_CONFIG.get('BROKER_URL'), backend=CELERY_CONFIG.get('RESULT_BACKEND'))

celery.conf.beat_schedule = {
    'refresh-tweets-every-15-minutes': {
        'task': 'tasks.refresh_tweets',
        'schedule': 60.0 * 15.0
    },
}
celery.conf.timezone = 'CET'

def get_tweets(client, start_time, end_time, next_token=None):
    return client.get_users_tweets(
        id='258856900', # JJansaSDS user ID
        max_results=100, # get 100 tweets at once
        pagination_token=next_token,
        start_time=start_time, # must be format YYYY-MM-DDTHH:mm:ssZ
        end_time=end_time,
        tweet_fields=['created_at', 'text', 'referenced_tweets', 'author_id', 'public_metrics', 'entities'],
        expansions=['referenced_tweets.id','author_id'] # add 'referenced_tweets.id.author_id' to get user data
    )

def get_tweets_from_id_list(client, id_list):
    return client.get_tweets(
        id_list,
        tweet_fields=['created_at', 'text', 'referenced_tweets', 'author_id', 'public_metrics', 'entities'],
        expansions=['referenced_tweets.id','author_id']
    )

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def resolve_url_for_tweet(tweet):

    logger.info(f'resolving tweet <{get_tweet_id(tweet)}>')
    result = get_urls_from_tweet(tweet)

    # store url(s)
    if result:
        logger.info(result)

@shared_task
def store_tweets(tweets, includes):
    for tweet in tweets:
        db_tweet, created = Tweet.objects.get_or_create(twitter_id=tweet.id)

        # delete related urls
        Url.objects.filter(tweet=db_tweet).delete()

        db_tweet.user_handle = 'JJansaSDS'
        db_tweet.timestamp = tweet.created_at
        db_tweet.text = tweet.text

        referenced_tweets = tweet.referenced_tweets

        if referenced_tweets and len(referenced_tweets) > 0:
            if referenced_tweets[0].type == "retweeted":
                db_tweet.retweet = True
                db_tweet.retweet_id = referenced_tweets[0].id
            elif referenced_tweets[0].type == "quoted":
                db_tweet.quote = True
                urls = tweet.entities['urls']
                db_tweet.quote_url = urls[len(urls)-1]['url'] # get the last url because this is the url of quoted tweet
        else:
            if tweet.entities and 'urls' in tweet.entities:
                for url in tweet.entities['urls']:
                    if not url['display_url'].startswith('pic.twitter'):
                        db_url = Url(short_url=url['url'], domain=get_domain_from_url(url['expanded_url']), tweet=db_tweet)
                        db_url.save()

        db_tweet.favorite_count = tweet.public_metrics['like_count']
        db_tweet.retweet_count = tweet.public_metrics['retweet_count']

        db_tweet.save()

    # additional information about referenced (retweeted and quoted) tweets
    for tweet in includes:
        qs = Tweet.objects.filter(retweet_id=tweet.id)
        if len(qs): # if this is a retweet we found the original tweet by retweet_id
            ot = qs[0]
            ot.retweet_timestamp = tweet.created_at
            referenced_tweets = tweet.referenced_tweets
            if referenced_tweets and len(referenced_tweets) > 0:
                if referenced_tweets[0].type == "quoted":
                    ot.retweet_quote = True
                    urls = tweet.entities['urls']
                    ot.retweet_quote_url = urls[len(urls)-1]['url']
            ot.save()

@shared_task
def refresh_tweets_on_date_string(date_string):
    if not is_valid_date_string(date_string):
        raise ValueError(f'The provided date ({date_string}) could not be parsed.')

    client = tweepy.Client(os.getenv('CLIENT_TOKEN', ''))

    start_time = start_in_iso_utc_format(date_string)
    end_time = end_in_iso_utc_format(date_string)
    
    result = get_tweets(client, start_time, end_time)

    if not result.data:
        print("Tweets not available!")
        return
    
    while result:
        tweets = result.data
        includes = result.includes['tweets']
        store_tweets(tweets, includes)

        # next page of results
        next_token = result.meta.get('next_token', None)
        if next_token:
            result = get_tweets(client, start_time, end_time, next_token=next_token)
        else:
            result = None

        # calculate daily summary
        daily_time(date_string)


@shared_task
def refresh_tweets():
    now_string = now().strftime('%Y-%m-%d')
    logger.info(f'START Fetching tweets for {now_string} ...')
    refresh_tweets_on_date_string(now_string)
    logger.info(f'END Fetching tweets for {now_string} ...')
