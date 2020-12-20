from flask import Flask, jsonify, abort, Response
from flask_cors import CORS
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand, Manager

from config import CACHE_CONFIG

import os
from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
apps.populate(settings.INSTALLED_APPS)

from utils import is_valid_date, SummaryCacheInfo, DateCacheInfo
from tweets import get_summary_date_range, get_gap_date_range, group_by_day, get_all_calculations, get_gaps, get_hashtags, get_start_of_day
from dmi_tcat import fetch_tweets_for_date_string
from stats.models import DailySums
from datetime import date, datetime, timedelta
from utils import SummaryCacheInfo, DateCacheInfo
from tweets import get_date_range, group_by_day, get_all_calculations, get_longest_gap, get_current_gap
from dmi_tcat import fetch_tweets_for_date
from tasks import resolve_urls_for_date, resolve_urls_for_all_tweets

app = Flask(__name__)
CORS(app)

app.config.from_mapping(CACHE_CONFIG)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)


@app.route('/robots.txt', methods=['GET'])
@cache.cached()
def robots():
  return Response('User-agent: *\nDisallow: /', mimetype="text/plain")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

# example model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)


@app.route('/<date>', methods=['GET'])
@cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date):
  tweets = fetch_tweets_for_date(date)
  calculations = get_all_calculations(tweets)

  # resolve urls
  # TODO move to scheduler
  resolve_urls_for_all_tweets.delay()

  return jsonify(tweets=tweets, calculations=calculations)

@app.route('/summary', methods=['GET'])
@cache.cached(forced_update=SummaryCacheInfo.should_force_update)
def summary():
  start, end = get_summary_date_range()
  tweets = fetch_tweets_for_date_string(start, end)

  tweets_by_day = group_by_day(tweets)
  calculations_by_day = {}

  for day, tweets in tweets_by_day.items():
    calculations_by_day[day] = get_all_calculations(tweets)

  return jsonify(calculations_by_day)

@app.route('/running-gap', methods=['GET'])
@cache.cached(timeout=1 * 60)
def running_gap():
  start, end = get_gap_date_range()
  tweets = fetch_tweets_for_date_string(start, end)
  gaps = get_gaps(tweets)

  return jsonify(gaps)

@app.route('/', defaults={'date': ''})
@app.route('/<date>', methods=['GET'])
@cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date):
  if not is_valid_date(date):
    abort(404)

  tweets = fetch_tweets_for_date_string(date)
  calculations = get_all_calculations(tweets)
  hashtags = get_hashtags(tweets)
  start_of_day = get_start_of_day(date)

  return jsonify(tweets=tweets, calculations=calculations, hashtags=hashtags, start_of_day=start_of_day)
