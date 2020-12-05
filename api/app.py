from flask import Flask, jsonify
from flask_cors import CORS
from flask_caching import Cache
from config import CACHE_CONFIG
from datetime import datetime

from tweets import get_date_range, group_by_day, get_all_calculations
from dmi_tcat import fetch_tweets_for_date

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
  tweets = fetch_tweets_for_date(date)
  calculations = get_all_calculations(tweets)
  return jsonify(calculations)

def get_summary_cache_key():
  return datetime.now().strftime('%Y-%m-%d')

@app.route('/summary', methods=['GET'])
@cache.cached(make_cache_key=get_summary_cache_key)
def summary():
  start, end = get_date_range()
  tweets = fetch_tweets_for_date(start, end)

  tweets_by_day = group_by_day(tweets)
  calculations_by_day = {}

  for day, tweets in tweets_by_day.items():
    calculations_by_day[day] = get_all_calculations(tweets)

  return jsonify(calculations_by_day)

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)
