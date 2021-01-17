import unittest
import logging
import sys

from freezegun import freeze_time

from tweets.utilities import _calculate_time
from utils import DateCacheInfo, SummaryCacheInfo
from datetime import datetime


class TestSummaryCacheInfo(unittest.TestCase):
  def test_forces_update_on_date_change(self):
    # Setting a random future date first to get our starting point.
    with freeze_time('2022-01-14T10:00Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), True)

    # Still the same day, so the cache is valid still
    with freeze_time('2022-01-14T15:00Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)
    with freeze_time('2022-01-14T20:00Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)

    # Still the same day in UTC, but already next day in Slovenia
    with freeze_time('2022-01-14T23:30Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), True)
    with freeze_time('2022-01-15T00:30Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)

  def test_knows_about_DST(self):
    # Moving to a random future date first to get our starting point. It's
    # August, so Slovenia should be in DST, which is UTC+2.
    with freeze_time('2022-08-14T10:00Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), True)
    with freeze_time('2022-08-14T15:59Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)
    with freeze_time('2022-08-14T21:59Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)

    # This is one minute past midnight in Slovenia
    with freeze_time('2022-08-14T22:01Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), True)
    with freeze_time('2022-08-14T23:01Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)
    with freeze_time('2022-08-15T00:01Z'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)

  def test_resets_updated_time_when_updating(self):
    initial_date_string = '2022-08-14 16:01+00:00'

    with freeze_time(initial_date_string):
      self.assertEqual(SummaryCacheInfo.should_force_update(), True)
      # Above call returned True, so last_update should match current datetime
      self.assertEqual(SummaryCacheInfo.last_update, datetime.fromisoformat(initial_date_string))

    with freeze_time('2022-08-14 20:01+00:00'):
      self.assertEqual(SummaryCacheInfo.should_force_update(), False)
      # Above call returned False, so last_update should be unchanged
      self.assertEqual(SummaryCacheInfo.last_update, datetime.fromisoformat(initial_date_string))


class TestDateCacheInfo(unittest.TestCase):
  @freeze_time('2022-01-14')
  def test_does_not_force_update_for_past_dates(self):
      # All initial calls return True because there is no last update set yet,
      # but from there on, past dates consistently return False

      self.assertEqual(DateCacheInfo.should_force_update('2022-01-01'), True)
      self.assertEqual(DateCacheInfo.should_force_update('2022-01-01'), False)

      self.assertEqual(DateCacheInfo.should_force_update('2020-01-01'), True)
      self.assertEqual(DateCacheInfo.should_force_update('2020-01-01'), False)
      self.assertEqual(DateCacheInfo.should_force_update('2020-01-01'), False)

      self.assertEqual(DateCacheInfo.should_force_update('1989-04-16'), True)
      self.assertEqual(DateCacheInfo.should_force_update('1989-04-16'), False)
      self.assertEqual(DateCacheInfo.should_force_update('1989-04-16'), False)
      self.assertEqual(DateCacheInfo.should_force_update('1989-04-16'), False)

  @freeze_time('2022-01-15T07:12Z')
  def test_forces_update_every_15_minutes_for_today(self):
      # As before, first call returns True and sets the last update time
      self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), True)

      # Now, the call will return False
      self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), False)

      # Still False 14 minutes later
      with freeze_time('2022-01-15T07:26Z'):
        self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), False)

      # And then True 16 minutes later
      with freeze_time('2022-01-15T07:28Z'):
        self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), True)

      # And so on
      with freeze_time('2022-01-15T07:40Z'):
        self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), False)
      with freeze_time('2022-01-15T07:42Z'):
        self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), False)
      with freeze_time('2022-01-15T07:44Z'):
        self.assertEqual(DateCacheInfo.should_force_update('2022-01-15'), True)

  @freeze_time('2022-01-15T07:12Z')
  def test_forces_update_for_past_date_with_old_data(self):
      # Last time we fetched fresh data was just before midnight _in Slovenia_
      # on January 14th, so one hour earlier in UTC.
      DateCacheInfo.last_updates['2022-01-14'] = datetime.fromisoformat('2022-01-14 22:46+00:00')

      # Today is January 15th, it's 7 in the morning (set in decorator). If
      # someone tries to get data January 14th, we update the cache because even
      # though the date itself is already "yesterday", our last update was also
      # yesterday and Ivan could have tweeted in those last 15 minutes before
      # midnight.
      self.assertEqual(DateCacheInfo.should_force_update('2022-01-14'), True)

      # But now that the above call triggered a refresh, an identical one should
      # return False
      self.assertEqual(DateCacheInfo.should_force_update('2022-01-14'), False)


class TestCalculateTime(unittest.TestCase):
    def test_empty(self):
        time = _calculate_time([])
        self.assertEqual(time.seconds, 0)

    def test_single_lonely(self):
        tweets = [
          { "created_at": "2020-11-12 08:41:42" }
        ]
        time = _calculate_time(tweets)
        self.assertEqual(time.seconds, 300)

    def test_intervals(self):
        tweets = [
          # This interval spans 4:30, which is less than time for a single tweet,
          # so we add 5 minutes.
          { "created_at": "2020-11-12 08:41:00" },
          { "created_at": "2020-11-12 08:42:43" },
          { "created_at": "2020-11-12 08:43:44" },
          { "created_at": "2020-11-12 08:45:30" },

          # Single tweet - 5 minutes
          { "created_at": "2020-11-12 09:45:48" },

          # Another single tweet - 5 minutes
          { "created_at": "2020-11-12 10:45:48" },

          # This interval spans 7:48, so we add exactly that.
          { "created_at": "2020-11-12 11:45:00" },
          { "created_at": "2020-11-12 11:46:48" },
          { "created_at": "2020-11-12 11:47:48" },
          { "created_at": "2020-11-12 11:52:48" },

          # This interval spans 1:10, so we add 5 minutes again.
          { "created_at": "2020-11-12 22:45:48" },
          { "created_at": "2020-11-12 22:46:58" },
        ]
        time = _calculate_time(tweets)
        self.assertEqual(time.seconds, 1668)

if __name__ == '__main__':
    unittest.main()
