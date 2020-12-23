from flask import Flask, jsonify, abort, Response
from flask_cors import CORS
from flask_caching import Cache
from config import CACHE_CONFIG

from utils import is_valid_date, SummaryCacheInfo, DateCacheInfo
from tweets import get_summary_date_range, get_gap_date_range, group_by_day, get_all_calculations, get_gaps, get_hashtags, get_start_of_day
from dmi_tcat import fetch_tweets_for_date

app = Flask(__name__)
CORS(app)

app.config.from_mapping(CACHE_CONFIG)
cache = Cache(app)

@app.route('/robots.txt', methods=['GET'])
@cache.cached()
def robots():
  return Response('User-agent: *\nDisallow: /', mimetype="text/plain")

@app.route('/summary', methods=['GET'])
@cache.cached(forced_update=SummaryCacheInfo.should_force_update)
def summary():
  start, end = get_summary_date_range()
  tweets = fetch_tweets_for_date(start, end)

  tweets_by_day = group_by_day(tweets)
  calculations_by_day = {}

  for day, tweets in tweets_by_day.items():
    calculations_by_day[day] = get_all_calculations(tweets)

  return jsonify(calculations_by_day)

@app.route('/running-gap', methods=['GET'])
@cache.cached(timeout=1 * 60)
def running_gap():
  start, end = get_gap_date_range()
  tweets = fetch_tweets_for_date(start, end)
  gaps = get_gaps(tweets)

  return jsonify(gaps)

@app.route('/', defaults={'date': ''})
@app.route('/<date>', methods=['GET'])
@cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date):
  if not is_valid_date(date):
    abort(404)

  tweets = fetch_tweets_for_date(date)
  calculations = get_all_calculations(tweets)
  hashtags = get_hashtags(tweets)
  start_of_day = get_start_of_day(date)

  return jsonify(tweets=tweets, calculations=calculations, hashtags=hashtags, start_of_day=start_of_day)
