from flask import Flask, Response
from flask_cors import CORS
from flask_caching import Cache
from requests import get
from requests.auth import HTTPBasicAuth
import json
import csv
import codecs
from contextlib import closing
from config import DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD, CACHE_CONFIG
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config.from_mapping(CACHE_CONFIG)
cache = Cache(app)

def calculate_date_cache_key(date):
  app.logger.debug(f'Calculating cache key for {date}')
  if datetime.now().date() == datetime.strptime(date, '%Y-%m-%d').date():
    period = int(int(datetime.strftime(datetime.now(), '%M')) / 15)
    calculated_cache_key = datetime.strftime(datetime.now(), f'%Y-%m-%d %H {period}')
  else:
    calculated_cache_key = date
  app.logger.debug(f'CALCULATED CACHE KEY: {calculated_cache_key}')
  return calculated_cache_key

@app.route('/<date>', methods=['GET'])
@cache.cached(make_cache_key=calculate_date_cache_key)
def index(date):
  file_url = f'http://51.15.220.60/analysis/mod.export_tweets.php?dataset=ONLY_jjansasds&query=&url_query=&media_url_query=&exclude=&from_user_name=&from_user_lang=&lang=&exclude_from_user_name=&from_user_description=&from_source=&startdate={date}&enddate={date}&whattodo=export_tweets&exportSettings=&graph_resolution=day&outputformat=csv'
  with closing(get(file_url, stream=True, auth=HTTPBasicAuth(DMI_TCAT_USERNAME, DMI_TCAT_PASSWORD))) as stream:
    csv_reader = csv.DictReader(
        codecs.iterdecode(stream.iter_lines(), 'utf-8')
    )
    tweets = []
    for row in csv_reader:
      tweets.append(row)

  return Response(json.dumps(tweets), mimetype='application/json')

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)
