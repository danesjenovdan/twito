import json
from datetime import date, datetime, timedelta, timezone
from collections import defaultdict

import slovenian_time

from tweets.models import Tweet

RETWEET_PREFIX = 'RT '
MAX_TIME_BETWEEN_TWEETS = timedelta(minutes=5)
TIME_FOR_ONE_TWEET = timedelta(minutes=5)
DATE_FORMAT = "%Y-%m-%d"
TWEET_ID = '\ufeffid'


def _date_to_string(date):
  return date.strftime(DATE_FORMAT)

def _generate_intervals(tweets):
  all_sessions = []
  current_session = []

  for tweet in tweets:
    if len(current_session) == 0:
      current_session.append(tweet)
      continue

    current_tweet_time = tweet.timestamp
    previous_tweet_time = current_session[-1].timestamp
    time_difference = current_tweet_time - previous_tweet_time

    if time_difference > MAX_TIME_BETWEEN_TWEETS:
      all_sessions.append(current_session)
      current_session = []

    current_session.append(tweet)

  if current_session:
    all_sessions.append(current_session)

  return all_sessions

def _get_tweet_type(tweet):
  if tweet.retweet:
    return "retweet"
  elif tweet.quote:
    return "retweet_with_comment"
  else:
    return "tweet"

def _get_counts(tweets):
  counts = { "tweet": 0, "retweet": 0, "retweet_with_comment": 0 }

  for tweet in tweets:
    tweet_type = _get_tweet_type(tweet)
    counts[tweet_type] += 1

  return counts

def get_hashtags(tweets):
  hashtags = defaultdict(int)
  for tweet in tweets:
    words = map(lambda word: word.lower().replace('-', ''), tweet.text.split())

    for word in words:
      if word.startswith("#"):
        hashtags[word] += 1

  sorted_tuples = sorted(hashtags.items(), key=lambda hashtag: hashtag[1])

  sorted_hashtags = [{"hashtag": hashtag, "number": number} for hashtag, number in list(reversed(sorted_tuples))]

  return sorted_hashtags[0:5]

def _calculate_time(tweets):
  intervals = _generate_intervals(tweets)
  duration = timedelta()

  for interval in intervals:
    start = interval[0].timestamp
    end = interval[-1].timestamp
    duration += max(end - start, TIME_FOR_ONE_TWEET)

  return duration

def get_gaps(tweets):
  now = slovenian_time.now()
  last_tweet_time = tweets.order_by('-timestamp').first().timestamp

  current_gap = (now - last_tweet_time).seconds

  longest_gap = 0
  current_tweet_time = last_tweet_time
  previous_tweet_time = None
  for tweet in tweets.order_by('timestamp')[1:]:
    previous_tweet_time = current_tweet_time
    current_tweet_time = tweet.timestamp
    longest_gap = max((current_tweet_time - previous_tweet_time).seconds, longest_gap)

  return {
    'longest_gap': longest_gap,
    'current_gap': current_gap,
  }

def get_all_calculations(tweets):
  calculations = _get_counts(tweets)
  calculations["time"] = _calculate_time(tweets).seconds

  return calculations

def group_by_day(tweets):
  days = {}

  for tweet in tweets:
    tweet_time = tweet.timestamp
    date_string = _date_to_string(tweet_time.astimezone(slovenian_time.TIMEZONE))

    if date_string not in days.keys():
      days[date_string] = []

    days[date_string].append(tweet)

  return days

def get_summary_date_range(days=90):
  end_date = slovenian_time.now() - timedelta(days=1) # yesterday
  start_date = end_date - timedelta(days=days)

  return _date_to_string(start_date), _date_to_string(end_date)

def get_summary_dates(days=90):
  end_date = slovenian_time.end_of_date(slovenian_time.now()) - timedelta(days=1)
  start_date = slovenian_time.start_of_date(end_date) - timedelta(days=days)

  return start_date, end_date

def get_gap_date_range():
  end_date = slovenian_time.now()
  start_date = end_date - timedelta(days=1) # yesterday

  return start_date, end_date

def is_retweet(tweet):
    return tweet.get('text').find(RETWEET_PREFIX) != -1


def get_tweet_id(tweet):
    return tweet.get(TWEET_ID)
