import unittest
import logging
import sys

from freezegun import freeze_time

from tweets import _calculate_time
from utils import calculate_date_cache_key
from datetime import datetime

# logger = logging.getLogger()
# logger.level = logging.DEBUG
# logger.addHandler(logging.StreamHandler(sys.stdout))

class TestCacheKeyGeneration(unittest.TestCase):
  def test_returns_date_for_past_dates(self):
    self.assertEqual(calculate_date_cache_key("2019-12-25"), "2019-12-25")
    self.assertEqual(calculate_date_cache_key("2020-08-01"), "2020-08-01")
    self.assertEqual(calculate_date_cache_key("2020-10-03"), "2020-10-03")
    self.assertEqual(calculate_date_cache_key("2019-12-25"), "2019-12-25")
    self.assertEqual(calculate_date_cache_key("1980-05-04"), "1980-05-04")

  def test_returns_date_with_period_for_today(self):
    with freeze_time("2012-01-14 12:08:11"):
      self.assertEqual(calculate_date_cache_key("2012-01-14"), "2012-01-14 12 0")
    with freeze_time("2012-01-14 12:21:11"):
      self.assertEqual(calculate_date_cache_key("2012-01-14"), "2012-01-14 12 1")
    with freeze_time("2012-01-14 12:44:59"):
      self.assertEqual(calculate_date_cache_key("2012-01-14"), "2012-01-14 12 2")
    with freeze_time("2012-01-14 12:45:01"):
      self.assertEqual(calculate_date_cache_key("2012-01-14"), "2012-01-14 12 3")
    with freeze_time("2012-01-14 13:08:11"):
      self.assertEqual(calculate_date_cache_key("2012-01-14"), "2012-01-14 13 0")

  def test_returns_date_with_period_for_tomorrow(self):
    with freeze_time("2012-01-14 23:58:11"):
      self.assertEqual(calculate_date_cache_key("2012-01-15"), "2012-01-14 23 3")


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
