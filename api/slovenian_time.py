from datetime import datetime
from pytz import timezone

TIMEZONE = timezone('CET')

def now():
  return datetime.now(tz=TIMEZONE)

def beginning_of_time():
  return datetime.fromtimestamp(0, tz=TIMEZONE)

def start_of_date_string(date_string):
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


def end_of_date_string(date_string):
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

def start_of_date(timestamp):
  return datetime(
    timestamp.year,
    timestamp.month,
    timestamp.day,
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
    tzinfo=TIMEZONE,
  )


def end_of_date(timestamp):
  return datetime(
    timestamp.year,
    timestamp.month,
    timestamp.day,
    hour=23,
    minute=59,
    second=59,
    microsecond=999999,
    tzinfo=TIMEZONE,
  )

def get_cet_time_from_twint_datestring(datestring):
    return datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S %Z').astimezone(timezone('CET'))
