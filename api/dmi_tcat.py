import csv
import codecs
from datetime import datetime, timedelta, timezone

from requests.auth import HTTPBasicAuth
from contextlib import closing
from requests import get

from config import DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD
import slovenian_time


def fetch_tweets_for_date_string(start_date_string, end_date_string=None):
  if not end_date_string:
    end_date_string = start_date_string

  slo_start = slovenian_time.start_of_day(start_date_string)
  slo_end = slovenian_time.end_of_day(end_date_string)

  # DMI-TCAT query params are UTC, so we need to fetch an additional day as last
  # one/two hours of the same day in UTC are already in the next day in CET.
  day_before_start = datetime.fromisoformat(start_date_string) - timedelta(days=1)
  start_query = day_before_start.strftime('%Y-%m-%d')
  end_query = end

  file_url = f'http://51.15.220.60/analysis/mod.export_tweets.php?dataset=ONLY_jjansasds&query=&url_query=&media_url_query=&exclude=&from_user_name=&from_user_lang=&lang=&exclude_from_user_name=&from_user_description=&from_source=&startdate={start_query}&enddate={end_query}&whattodo=export_tweets&exportSettings=&graph_resolution=day&outputformat=csv'
  with closing(get(file_url, stream=True, auth=HTTPBasicAuth(DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD))) as stream:
    csv_reader = csv.DictReader(
      codecs.iterdecode(stream.iter_lines(), 'utf-8')
    )
    tweets = []
    for row in csv_reader:
      # The date returned from DMI-TCAT doesn't include any timezone info, but
      # we know for a fact it's in UTC, so let's specify that explicitly
      row["created_at"] = "T".join(row["created_at"].split(" ")) + "+00:00"
      tweet_time = datetime.fromisoformat(row["created_at"])
      if slo_start < tweet_time < slo_end:
        tweets.append(row)

  return tweets
