from datetime import timedelta, datetime

import slovenian_time

def is_valid_date(string):
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
    return slovenian_time.end_of_day(date_string) < slovenian_time.now()

  @classmethod
  def should_force_update(self, date):
    if not is_valid_date(date):
      return False

    date_passed_in_slo = self.date_passed_in_slovenia(date)
    last_updated_after_date = self.get_last_update(date) > slovenian_time.end_of_day(date)

    if date_passed_in_slo and last_updated_after_date:
      return False

    time_since_last_update = slovenian_time.now() - self.get_last_update(date)

    if time_since_last_update > self.TODAYS_CACHE_PERIOD:
      self.set_last_update(date)
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
