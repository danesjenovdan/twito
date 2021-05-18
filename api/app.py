import os

from flask import Flask, jsonify, abort, Response
from flask_cors import CORS
from flask_caching import Cache

from django.apps import apps
from django.conf import settings
from django.forms.models import model_to_dict

import twint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
apps.populate(settings.INSTALLED_APPS)

from settings import CACHE_CONFIG

from utils import is_valid_date_string, SummaryCacheInfo, DateCacheInfo, tomorrow, full_tweet_text
from tweets.utilities import get_summary_date_range, get_summary_dates, get_gap_date_range, group_by_day, get_all_calculations, get_gaps, get_hashtags

from datetime import datetime, timedelta
from slovenian_time import get_cet_time_from_twint_datestring, TIMEZONE, start_of_date, end_of_date, now, start_of_date_string, end_of_date_string

from tweets.models import Tweet

app = Flask(__name__)
CORS(app)

app.config.from_mapping(CACHE_CONFIG)
cache = Cache(app)

@app.route('/robots.txt', methods=['GET'])
@cache.cached()
def robots():
  return Response('User-agent: *\nDisallow: /', mimetype="text/plain")


@app.route('/summary', methods=['GET'])
@cache.cached(forced_update=SummaryCacheInfo.should_force_update)
def summary():
  start, end = get_summary_dates()
  tweets = Tweet.objects.filter(timestamp__gte=start, timestamp__lte=end)

  tweets_by_day = group_by_day(tweets)
  calculations_by_day = {}

  for day, tweets in tweets_by_day.items():
      calculations_by_day[day] = get_all_calculations(tweets)

  return jsonify(calculations_by_day)


@app.route('/running-gap', methods=['GET'])
@cache.cached(timeout=1 * 60)
def running_gap():
  start, end = get_gap_date_range()
  tweets = Tweet.objects.filter(timestamp__gte=start, timestamp__lte=end)
  gaps = get_gaps(tweets)

  return jsonify(gaps)

@app.route('/', defaults={'date_string': ''})
@app.route('/<date_string>', methods=['GET'])
@cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date_string):
  if not is_valid_date_string(date_string):
    abort(404)

  start = start_of_date_string(date_string)
  end = end_of_date_string(date_string)

  tweets = Tweet.objects.filter(timestamp__gte=start, timestamp__lte=end)
  calculations = get_all_calculations(tweets)
  hashtags = get_hashtags(tweets)

  jsonable_tweets = [model_to_dict(tweet) for tweet in tweets]

  return jsonify(tweets=jsonable_tweets, calculations=calculations, hashtags=hashtags, start_of_day=start)

@app.route('/twint-test', defaults={'date_string': ''})
@app.route('/twint-test/<date_string>', methods=['GET'])
def twint_test(date_string):
  if not is_valid_date_string(date_string):
    abort(404)

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
  
  tweets_jsonable = [{
    # common info
    'twitter_id': tweet.id_str,
    'timestamp': get_cet_time_from_twint_datestring(tweet.datetime),
    'text': full_tweet_text(tweet),

    # retweet info
    'retweet': tweet.retweet,
    'retweet_timestamp': get_cet_time_from_twint_datestring(tweet.retweet_date) if tweet.retweet else None,
    'retweet_id': tweet.retweet_id if tweet.retweet else None,
    'retweet_quote': bool(tweet.quote_url) and tweet.retweet,
    'retweet_quote_url': tweet.quote_url if bool(tweet.quote_url) and tweet.retweet else None,

    # quote info
    'quote': bool(tweet.quote_url) and not tweet.retweet,
    'quote_url': tweet.quote_url if bool(tweet.quote_url) and not tweet.retweet else None,

    # likes and retweets counts
    'likes': tweet.likes_count,
    'retweets': tweet.retweets_count,

    # debug info
    # 'vars': vars(tweet),
  } for tweet in tweets]

  return jsonify(tweets_jsonable)
