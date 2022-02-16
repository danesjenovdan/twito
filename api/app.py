import os

from flask import Flask, jsonify, abort, Response
from flask_cors import CORS
from flask_caching import Cache
from flask.cli import with_appcontext
import click


from django.apps import apps
from django.conf import settings
from django.forms.models import model_to_dict

from datetime import date, timedelta

# import tweepy
# from pytz import timezone


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
apps.populate(settings.INSTALLED_APPS)

from settings import CACHE_CONFIG

from utils import is_valid_date_string, SummaryCacheInfo, DateCacheInfo, tomorrow, full_tweet_text
from tweets.utilities import (
  get_summary_date_range, 
  get_summary_dates, 
  get_gap_date_range, 
  group_by_day, 
  get_all_calculations, 
  get_gaps, 
  get_hashtags,
  get_domains,
  get_avg_time_summary,
  get_avg_tweet_summary,
  get_avg_time_summary_since_pandemic,
  get_avg_tweet_summary_since_pandemic,
  get_avg_tweets_trend,
  get_retweets,
  tweet_per_day_trend,
  time_per_day_trend,
  get_avg_tweets_trend_since_pandemic,
  get_avg_time_summary_trend,
  get_avg_time_summary_trend_since_pandemic,
  daily_time
)

from datetime import datetime, timedelta
from slovenian_time import get_cet_time_from_twint_datestring, TIMEZONE, start_of_date, end_of_date, now, start_of_date_string, end_of_date_string, get_yesterday
from utils import is_valid_date_string
from tasks import refresh_tweets_on_date_string

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

@app.route('/fetch-analysis', methods=['GET'])
# @cache.cached(timeout=1 * 60)
def get_analysis():
  avg_tweet_summary = get_avg_tweet_summary()
  avg_tweets_trend, avg_tweets_trend_percentage = get_avg_tweets_trend()
  avg_tweet_summary_pandemic = get_avg_tweet_summary_since_pandemic()
  avg_tweets_trend_since_pandemic, avg_tweets_trend_since_pandemic_percentage = get_avg_tweets_trend_since_pandemic()
  avg_time_summary = get_avg_time_summary()
  avg_time_summary_trend, avg_time_summary_trend_percentage = get_avg_time_summary_trend()
  avg_time_summary_pandemic = get_avg_time_summary_since_pandemic()
  avg_time_trend_since_pandemic, avg_time_trend_since_pandemic_percentage = get_avg_time_summary_trend_since_pandemic()

  return jsonify(
    avg_tweet_summary=avg_tweet_summary,
    avg_time_summary=avg_time_summary, 
    avg_tweet_summary_pandemic=avg_tweet_summary_pandemic,
    avg_time_summary_pandemic=avg_time_summary_pandemic,
    avg_tweets_trend=avg_tweets_trend,
    avg_tweets_trend_percentage=avg_tweets_trend_percentage,
    avg_tweets_trend_since_pandemic=avg_tweets_trend_since_pandemic,
    avg_tweets_trend_since_pandemic_percentage=avg_tweets_trend_since_pandemic_percentage,
    avg_time_summary_trend=avg_time_summary_trend,
    avg_time_summary_trend_percentage=avg_time_summary_trend_percentage,
    avg_time_trend_since_pandemic=avg_time_trend_since_pandemic,
    avg_time_trend_since_pandemic_percentage=avg_time_trend_since_pandemic_percentage
  )

@app.route('/', defaults={'date_string': ''})
@app.route('/<date_string>', methods=['GET'])
@cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date_string):
  if not is_valid_date_string(date_string):
    abort(404)

  start = start_of_date_string(date_string)
  end = end_of_date_string(date_string)

  # refresh_tweets_on_date_string(date_string)

  tweets = Tweet.objects.filter(timestamp__gte=start, timestamp__lte=end)
  calculations = get_all_calculations(tweets)
  hashtags = get_hashtags(tweets)
  retweets = Tweet.objects.filter(timestamp__gte=start, timestamp__lte=end, retweet=True)
  retweeted_users = get_retweets(retweets)
  domains = get_domains(tweets)
  trendTweetsNo, trendTweetsPercentage = tweet_per_day_trend(date_string)
  trendTime, trendTimePercentage = time_per_day_trend(date_string)

  jsonable_tweets = [{
    'id': tweet.id,
    'retweet_id': tweet.retweet_id,
    'twitter_id': tweet.twitter_id,
    'quote': tweet.quote,
    'quote_url': tweet.quote_url,
    'retweet': tweet.retweet,
    'retweet_count': tweet.retweet_count,
    'retweet_quote': tweet.retweet_quote,
    'retweet_quote_url': tweet.retweet_quote_url,
    'retweet_timestamp': tweet.retweet_timestamp.isoformat() if tweet.retweet_timestamp else None,
    'timestamp': tweet.timestamp.isoformat(), # tweet.timestamp.astimezone(timezone('CET')).isoformat(),
    'favorite_count': tweet.favorite_count,
    'text': tweet.text,
  } for tweet in tweets]

  return jsonify(
    tweets=jsonable_tweets, 
    calculations=calculations, 
    hashtags=hashtags, 
    retweeted_users=retweeted_users, 
    domains=domains, 
    trendTweetsNo=trendTweetsNo,
    trendTweetsPercentage=trendTweetsPercentage,
    trendTime=trendTime,
    trendTimePercentage=trendTimePercentage,
    start_of_day=start.isoformat()
  )

# @app.route('/calculate-daily-summaries', methods=['GET'])
# def calculate_daily_summaries():
#   start_date = date(2022, 2, 1)
#   end_date = date(2022, 2, 16)
#   delta = timedelta(days=1)
#   while start_date <= end_date:
#     print(start_date.strftime("%Y-%m-%d"))
#     refresh_tweets_on_date_string(start_date.strftime("%Y-%m-%d"))
#     start_date += delta

#   return jsonify(
#     message="success"
#   )

# command to calculate daily summaries from start_date to end_date
# both start_date and end_date are included!
@click.command(name='calculate_daily_summaries')
@click.argument('start_date_string')
@click.argument('end_date_string')
@with_appcontext
def calculate_daily_summaries(start_date_string, end_date_string):
  if not is_valid_date_string(start_date_string):
    raise ValueError(f'The provided date ({start_date_string}) could not be parsed.')
  if not is_valid_date_string(end_date_string):
    raise ValueError(f'The provided date ({end_date_string}) could not be parsed.')

  delta = timedelta(days=1)
  start_date = datetime.strptime(start_date_string, "%Y-%m-%d").date()
  end_date = datetime.strptime(end_date_string, "%Y-%m-%d").date()

  while start_date <= end_date:
    time = daily_time(start_date.strftime("%Y-%m-%d"))
    print(start_date.strftime("%Y-%m-%d"), ':', time)
    start_date += delta
 
# command to get tweets from start_date to end_date
# both start_date and end_date are included!
@click.command(name='get_tweets')
@click.argument('start_date_string')
@click.argument('end_date_string')
@with_appcontext
def get_tweets(start_date_string, end_date_string):
  if not is_valid_date_string(start_date_string):
    raise ValueError(f'The provided date ({start_date_string}) could not be parsed.')
  if not is_valid_date_string(end_date_string):
    raise ValueError(f'The provided date ({end_date_string}) could not be parsed.')

  delta = timedelta(days=1)
  start_date = datetime.strptime(start_date_string, "%Y-%m-%d").date()
  end_date = datetime.strptime(end_date_string, "%Y-%m-%d").date()

  while start_date <= end_date:
    print(start_date.strftime("%Y-%m-%d"), 'start')
    refresh_tweets_on_date_string(start_date.strftime("%Y-%m-%d"))
    print(start_date.strftime("%Y-%m-%d"), 'done')
    start_date += delta

app.cli.add_command(calculate_daily_summaries)
app.cli.add_command(get_tweets)

# @app.route('/twint-test', defaults={'date_string': ''})
# @app.route('/twint-test/<date_string>', methods=['GET'])
# def twint_test(date_string):
#   if not is_valid_date_string(date_string):
#     abort(404)

#   tweets = []

#   twint_config = twint.Config()
#   twint_config.Hide_output = True
#   twint_config.Store_object = True
#   twint_config.Store_object_tweets_list = tweets
#   twint_config.Username = "jjansasds"
#   twint_config.Since = date_string
#   twint_config.Until = tomorrow(date_string)

#   # Run
#   # twint.run.Profile(twint_config)
#   twint.run.Profile(twint_config)
  
#   tweets_jsonable = [{
#     # common info
#     'twitter_id': tweet.id_str,
#     'timestamp': get_cet_time_from_twint_datestring(tweet.datetime),
#     'text': full_tweet_text(tweet),

#     # retweet info
#     'retweet': tweet.retweet,
#     'retweet_timestamp': get_cet_time_from_twint_datestring(tweet.retweet_date) if tweet.retweet else None,
#     'retweet_id': tweet.retweet_id if tweet.retweet else None,
#     'retweet_quote': bool(tweet.quote_url) and tweet.retweet,
#     'retweet_quote_url': tweet.quote_url if bool(tweet.quote_url) and tweet.retweet else None,

#     # quote info
#     'quote': bool(tweet.quote_url) and not tweet.retweet,
#     'quote_url': tweet.quote_url if bool(tweet.quote_url) and not tweet.retweet else None,

#     # likes and retweets counts
#     'likes': tweet.likes_count,
#     'retweets': tweet.retweets_count,

#     # debug info
#     # 'vars': vars(tweet),
#   } for tweet in tweets]

#   return jsonify(tweets_jsonable)
