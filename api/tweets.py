import json
from datetime import date, datetime, timedelta

RETWEET_PREFIX = 'RT '
MAX_TIME_BETWEEN_TWEETS = timedelta(minutes=5)
TIME_FOR_ONE_TWEET = timedelta(minutes=2)

def _generate_intervals(tweets):
  all_sessions = []
  current_session = []

  for tweet in tweets:
    if len(current_session) == 0:
      current_session.append(tweet)
      continue

    current_tweet_time = datetime.fromisoformat(tweet["created_at"])
    previous_tweet_time = datetime.fromisoformat(current_session[-1]["created_at"])
    time_difference = current_tweet_time - previous_tweet_time

    if time_difference > MAX_TIME_BETWEEN_TWEETS:
      all_sessions.append(current_session)
      current_session = []

    current_session.append(tweet)

  if current_session:
    all_sessions.append(current_session)

  return all_sessions

def _get_tweet_type(tweet):
  if tweet["text"].startswith(RETWEET_PREFIX):
    return "retweet"
  elif tweet["quoted_status_id"] != "":
    return "retweet_with_comment"
  else:
    return "tweet"

def _get_counts(tweets):
  counts = { "tweet": 0, "retweet": 0, "retweet_with_comment": 0 }

  for tweet in tweets:
    tweet_type = _get_tweet_type(tweet)
    counts[tweet_type] += 1

  return counts

def _calculate_time(tweets):
  intervals = _generate_intervals(tweets)
  duration = timedelta()

  for interval in intervals:
    if (len(interval) == 1):
      # Lone tweet, append default time
      duration += TIME_FOR_ONE_TWEET
      continue

    start = datetime.fromisoformat(interval[0]["created_at"])
    end = datetime.fromisoformat(interval[-1]["created_at"])
    duration += end - start

  return duration

def get_all_calculations(tweets):
  calculations = _get_counts(tweets)
  calculations["time"] = _calculate_time(tweets).seconds
  return calculations

def group_by_day(tweets):
  days = {}

  for tweet in tweets:
    date = tweet["created_at"].split(" ", 1)[0]

    if date not in days:
      days[date] = []

    days[date].append(tweet)

  return days

def get_date_range(days=90):
  end_date = date.today()
  start_date = end_date - timedelta(days=days)
  date_format = "%Y-%m-%d"

  end = end_date.strftime(date_format)
  start =  start_date.strftime(date_format)

  return start, end


