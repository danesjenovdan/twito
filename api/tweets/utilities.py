from datetime import datetime, timedelta
from collections import defaultdict
from django.db.models import Count, Avg

import slovenian_time

from tweets.models import Tweet, Url, DailySummary

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

def get_domains(tweets):
  domains = list(Url.objects.filter(tweet__in=tweets).values('domain').annotate(domain_num=Count('domain')).order_by('domain')[:5])
  sorted_domains = list(reversed(sorted(domains, key=lambda i: i['domain_num'])))
  return sorted_domains

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

def get_retweets(tweets):
  retweets = defaultdict(int)
  for tweet in tweets:
    words = map(lambda word: word.lower().replace('-', ''), tweet.text.split())

    for word in words:
      if word.startswith("@"):
        retweets[word] += 1
        break

  sorted_tuples = sorted(retweets.items(), key=lambda retweet: retweet[1])
  sorted_retweets = [{"tag": retweet[:-1], "number": number} for retweet, number in list(reversed(sorted_tuples))]
  return sorted_retweets[0:5]

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

def daily_time(date_string):
  (year, month, day) = [int(date_part) for date_part in date_string.split("-")]
  date = datetime(year, month, day)
  start_date = slovenian_time.start_of_date_string(date_string)
  end_date = slovenian_time.end_of_date_string(date_string)
  tweets = Tweet.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)
  time = _calculate_time(tweets).seconds
  ds, created = DailySummary.objects.get_or_create(date=date)
  ds.time = time
  ds.save()
  return ds.time

def get_all_calculations(tweets):
  calculations = _get_counts(tweets)
  calculations["time"] = _calculate_time(tweets).seconds
  return calculations

def get_avg_tweet_summary():
  # average including today
  qs = Tweet.objects.values('timestamp__date').annotate(total=Count('id')).aggregate(Avg('total'))
  return round(qs['total__avg'])

def get_avg_tweets_trend():
  # average including yesterday, but not today
  avg_today = get_avg_tweet_summary()
  avg_yesterday = round(Tweet.objects.filter(timestamp__date__lt=slovenian_time.now()).values('timestamp__date').annotate(total=Count('id')).aggregate(Avg('total'))['total__avg'])
  difference = avg_today - avg_yesterday
  if avg_yesterday == 0:
    return (difference, None)
  else:
    percentage = round((difference / avg_yesterday) * 100)
    return (difference, percentage)

def get_avg_tweet_summary_since_pandemic():
  qs = Tweet.objects.filter(timestamp__date__gte=datetime(2020, 3, 12)).values('timestamp__date').annotate(total=Count('id')).aggregate(Avg('total'))
  return round(qs['total__avg'])

def get_avg_tweets_trend_since_pandemic():
  avg_today = get_avg_tweet_summary_since_pandemic()
  avg_yesterday = round(Tweet.objects.filter(timestamp__date__gte=datetime(2020, 3, 12), timestamp__date__lt=slovenian_time.now()).values('timestamp__date').annotate(total=Count('id')).aggregate(Avg('total'))['total__avg'])
  difference = avg_today - avg_yesterday
  if avg_yesterday == 0:
    return (difference, None)
  else:
    percentage = round((difference / avg_yesterday) * 100)
    return (difference, percentage)

def get_avg_time_summary():
  qs = DailySummary.objects.all().aggregate(Avg('time'))
  if qs['time__avg']:
    return round(qs['time__avg'])
  return None

def get_avg_time_summary_trend():
  # average time spent on twitter until today
  avg_today = get_avg_time_summary()
  # average time spent on twitter until end of yesterday
  qs = DailySummary.objects.filter(date__lt=slovenian_time.now()).aggregate(Avg('time'))['time__avg']
  # if daily summaries do not exist return None
  if not qs:
    return (None, None)
  avg_yesterday = round(qs)
  difference = avg_today - avg_yesterday
  # make sure we don't divide by zero
  if avg_yesterday == 0:
    return (difference, None)
  else:
    percentage = round((difference / avg_yesterday) * 100)
    return (difference, percentage)

def get_avg_time_summary_since_pandemic():
  qs = DailySummary.objects.filter(date__gte=datetime(2020, 3, 12)).aggregate(Avg('time'))
  if qs['time__avg']:
    return round(qs['time__avg'])
  return None

def get_avg_time_summary_trend_since_pandemic():
  # average time spent on twitter since start of the pandemic until today
  avg_today = get_avg_time_summary_since_pandemic()
  # average time spent on twitter since start of the pandemic until end of yesterday
  qs = DailySummary.objects.filter(date__gte=datetime(2020, 3, 12), date__lt=slovenian_time.now()).aggregate(Avg('time'))['time__avg']
  # if daily summaries do not exist return None
  if not qs:
    return (None, None)
  avg_yesterday = round(qs)
  difference = avg_today - avg_yesterday
  # make sure we don't divide by zero
  if avg_yesterday == 0:
    return (difference, None)
  else:
    percentage = round((difference / avg_yesterday) * 100)
    return (difference, percentage)

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

def tweet_per_day_trend(date_string):
  today = slovenian_time.start_of_date_string(date_string)
  yesterday = slovenian_time.get_yesterday(date_string)
  try:
    no_of_tweets_yesterday = Tweet.objects.filter(timestamp__gte=slovenian_time.start_of_date(yesterday), timestamp__lte=slovenian_time.end_of_date(yesterday)).count()
    no_of_tweets_today = Tweet.objects.filter(timestamp__gte=slovenian_time.start_of_date(today), timestamp__lte=slovenian_time.end_of_date(today)).count()
    if no_of_tweets_yesterday == 0:
      return (difference, None)
    else:
      difference = no_of_tweets_today - no_of_tweets_yesterday
      percentage = round((difference / no_of_tweets_yesterday) * 100)
      return (difference, percentage)
  except:
    return (0, 0)
  
def time_per_day_trend(date_string):
  (year, month, day) = [int(date_part) for date_part in date_string.split("-")]
  date = datetime(year, month, day)
  date_before =  date - timedelta(days=1)
  try:
    time_yesterday = DailySummary.objects.get(date=date_before).time
    time_today = DailySummary.objects.get(date=date).time
    difference = time_today - time_yesterday
    if time_yesterday == 0:
      return (difference, None)
    else:
      percentage = round((difference / time_yesterday) * 100)
      return (difference, percentage)
  except:
    return (0, 0)
