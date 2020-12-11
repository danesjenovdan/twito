import json
from datetime import date, datetime, timedelta
from collections import defaultdict

RETWEET_PREFIX = 'RT '
MAX_TIME_BETWEEN_TWEETS = timedelta(minutes=5)
TIME_FOR_ONE_TWEET = timedelta(minutes=5)

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

def _get_hashtags(tweets):
  hashtags = defaultdict(int)
  for tweet in tweets:
    words = map(lambda word: word.lower().replace('-', ''), tweet["text"].split())

    for word in words:
      if word.startswith("#"):
        hashtags[word] += 1

  sorted_tuples = sorted(hashtags.items(), key=lambda hashtag: hashtag[1])

  sorted_hashtags = [{"hashtag": hashtag, "number": number} for hashtag, number in list(reversed(sorted_tuples))]

  return sorted_hashtags

def _calculate_time(tweets):
  intervals = _generate_intervals(tweets)
  duration = timedelta()

  for interval in intervals:
    start = datetime.fromisoformat(interval[0]["created_at"])
    end = datetime.fromisoformat(interval[-1]["created_at"])
    duration += max(end - start, TIME_FOR_ONE_TWEET)

  return duration

def get_longest_gap(tweets):
  gap = 0
  current_tweet_time = datetime.fromisoformat(tweets[0]["created_at"])
  previous_tweet_time = None
  for tweet in tweets[1:]:
    previous_tweet_time = current_tweet_time
    current_tweet_time = datetime.fromisoformat(tweet["created_at"])
    gap = max((current_tweet_time - previous_tweet_time).seconds, gap)

  return gap

def get_current_gap(tweets):
  return (datetime.now() - datetime.fromisoformat(tweets[-1]["created_at"])).seconds
  # gap = 0
  # current_tweet_time = datetime.fromisoformat(tweets[0]["created_at"])
  # previous_tweet_time = None
  # for tweet in tweets[1:]:
  #   previous_tweet_time = current_tweet_time
  #   current_tweet_time = datetime.fromisoformat(tweet["created_at"])
  #   gap = max((current_tweet_time - previous_tweet_time).seconds, gap)

  # return gap


def get_all_calculations(tweets):
  calculations = _get_counts(tweets)
  calculations["time"] = _calculate_time(tweets).seconds
  calculations["hashtags"] = _get_hashtags(tweets)

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
