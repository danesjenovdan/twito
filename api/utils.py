from datetime import timedelta, datetime

import slovenian_time

def is_valid_date_string(string):
  try:
    datetime.strptime(string, "%Y-%m-%d")
    return True
  except:
    return False

class DateCacheInfo:
  TODAYS_CACHE_PERIOD = timedelta(minutes=15)
  last_updates = {}

  @staticmethod
  def date_passed_in_slovenia(date_string):
    return slovenian_time.end_of_date_string(date_string) < slovenian_time.now()

  @classmethod
  def should_force_update(self, date_string):
    if not is_valid_date_string(date_string):
      return False

    date_passed_in_slo = self.date_passed_in_slovenia(date_string)
    last_updated_after_date = self.get_last_update(date_string) > slovenian_time.end_of_date_string(date_string)

    if date_passed_in_slo and last_updated_after_date:
      return False

    time_since_last_update = slovenian_time.now() - self.get_last_update(date_string)

    if time_since_last_update > self.TODAYS_CACHE_PERIOD:
      self.set_last_update(date_string)
      return True

    return False

  @classmethod
  def get_last_update(self, date_string):
    return self.last_updates.get(date_string, slovenian_time.beginning_of_time())

  @classmethod
  def set_last_update(self, date_string):
    self.last_updates[date_string] = slovenian_time.now()


class SummaryCacheInfo:
  last_update = None

  @classmethod
  def should_force_update(self):
    now = slovenian_time.now()

    if not self.last_update or self.last_update.day != now.day:
      self.last_update = now
      return True

    return False

def tomorrow(date):
  return datetime.strftime(datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d')

def full_tweet_text(tweet):
  if not tweet.retweet:
    return tweet.tweet
  
  rt_prefix = tweet.tweet.split(': ')[0]
  return f'{rt_prefix}: {tweet.user_rt}'
