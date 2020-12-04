import json
from datetime import date
from dateutil.relativedelta import relativedelta

RETWEET_PREFIX = 'RT '

def _get_tweet_counts(tweets):
  counts = { "tweet": 0, "retweet": 0, "retweet_with_comment": 0 }

  for tweet in tweets:
    tweet_type = _get_tweet_type(tweet)
    counts[tweet_type] += 1

  return counts

def _get_tweet_type(tweet):
  if tweet["text"].startswith(RETWEET_PREFIX):
    return "retweet"
  elif "quotedStatusId" in tweet:
    return "retweet_with_comment"
  else:
    return "tweet"

def _group_by_day(tweets):
  days = {}

  for tweet in tweets:
    date = tweet["created_at"].split(" ", 1)[0]

    if date not in days:
      days[date] = []

    days[date].append(tweet)

  return days

def get_date_range(days=90):
  end_date = date.today()
  delta = relativedelta(days=days)
  start_date = end_date - delta
  date_format = "%Y-%m-%d"

  end = end_date.strftime(date_format)
  start =  start_date.strftime(date_format)

  return start, end

def group_and_count(tweets):
  tweets_by_day = _group_by_day(tweets)
  counts_by_day = { day: _get_tweet_counts(tweets) for day, tweets in tweets_by_day.items() }

  return counts_by_day
