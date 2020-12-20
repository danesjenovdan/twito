from datetime import datetime
from pytz import timezone

TIMEZONE = timezone('CET')

def now():
  return datetime.now(tz=TIMEZONE)

def beginning_of_time():
  return datetime.fromtimestamp(0, tz=TIMEZONE)

def start_of_day(date_string):
  (year, month, day) = [int(date_part) for date_part in date_string.split("-")]
  return datetime(
    year,
    month,
    day,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
    tzinfo=TIMEZONE,
  )


def end_of_day(date_string):
  (year, month, day) = [int(date_part) for date_part in date_string.split("-")]
  return datetime(
    year,
    month,
    day,
    hour=23,
    minute=59,
    second=59,
    microsecond=999999,
    tzinfo=TIMEZONE,
  )
