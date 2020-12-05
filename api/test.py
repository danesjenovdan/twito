import unittest
from tweets import _calculate_time

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
