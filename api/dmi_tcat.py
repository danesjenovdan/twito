import csv
import codecs

from requests.auth import HTTPBasicAuth
from contextlib import closing
from requests import get

from config import DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD

def fetch_tweets_for_date(start, end=None):
  if not end:
    end = start

  file_url = f'http://51.15.220.60/analysis/mod.export_tweets.php?dataset=ONLY_jjansasds&query=&url_query=&media_url_query=&exclude=&from_user_name=&from_user_lang=&lang=&exclude_from_user_name=&from_user_description=&from_source=&startdate={start}&enddate={end}&whattodo=export_tweets&exportSettings=&graph_resolution=day&outputformat=csv'
  with closing(get(file_url, stream=True, auth=HTTPBasicAuth(DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD))) as stream:
    csv_reader = csv.DictReader(
      codecs.iterdecode(stream.iter_lines(), 'utf-8')
    )
    tweets = []
    for row in csv_reader:
      tweets.append(row)

  return tweets
