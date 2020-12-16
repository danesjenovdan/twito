from datetime import datetime, timedelta, tzinfo
from pytz import timezone, country_timezones
import logging

logger = logging.getLogger(__name__)

SLOVENIAN_TIMEZONE = timezone('CET')
TODAYS_CACHE_PERIOD = 15 # minutes

class DateCacheInfo:
  last_updates = {}

  @staticmethod
  def get_end_of_day(date_string):
    (year, month, day) = [int(date_part) for date_part in date_string.split('-')]
    last_second_of_day = datetime(year, month, day, hour=23, minute=59, second=59, tzinfo=SLOVENIAN_TIMEZONE)

    return last_second_of_day

  @classmethod
  def date_passed_in_slovenia(self, date_string):
    return self.get_end_of_day(date_string) < datetime.now(tz=SLOVENIAN_TIMEZONE)

  @classmethod
  def should_force_update(self, date):
    date_passed_in_slo = self.date_passed_in_slovenia(date)
    last_updated_after_date = self.get_last_update(date) > self.get_end_of_day(date)

    if date_passed_in_slo and last_updated_after_date:
      return False

    time_since_last_update = datetime.now(tz=SLOVENIAN_TIMEZONE) - self.get_last_update(date)

    if time_since_last_update > timedelta(minutes=TODAYS_CACHE_PERIOD):
      self.set_last_update(date)
      return True

    return False

  @classmethod
  def get_last_update(self, date_string):
    return self.last_updates.get(date_string, datetime.fromtimestamp(0, tz=SLOVENIAN_TIMEZONE))

  @classmethod
  def set_last_update(self, date_string):
    self.last_updates[date_string] = datetime.now(tz=SLOVENIAN_TIMEZONE)


class SummaryCacheInfo:
  last_update = None

  @classmethod
  def should_force_update(self):
    now = datetime.now(tz=SLOVENIAN_TIMEZONE)

    if not self.last_update or self.last_update.day != now.day:
      self.last_update = now
      return True

    return False
