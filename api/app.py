from datetime import datetime, timedelta

from flask import Flask, jsonify
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate

from config import CACHE_CONFIG
from dmi_tcat import fetch_tweets_for_date
from models import db
from tasks import store_all_tweets
from tweets import get_date_range, group_by_day, get_all_calculations, get_longest_gap, get_current_gap
from utils import SummaryCacheInfo

app = Flask(__name__)
CORS(app)

app.config.from_mapping(CACHE_CONFIG)
migrate = Migrate(app, db)
cache = Cache(app)


@app.teardown_appcontext
def shutdown(response=None):
    db.remove()
    return response


@app.route('/<date>', methods=['GET'])
# @cache.cached(forced_update=DateCacheInfo.should_force_update)
def index(date):
    tweets = fetch_tweets_for_date(date)
    calculations = get_all_calculations(tweets)

    # TODO move to scheduler
    # resolve_urls_for_all_tweets.delay()
    store_all_tweets()

    return jsonify(tweets=tweets, calculations=calculations)


@app.route('/summary', methods=['GET'])
@cache.cached(forced_update=SummaryCacheInfo.should_force_update)
def summary():
    start, end = get_date_range()
    tweets = fetch_tweets_for_date(start, end)

    tweets_by_day = group_by_day(tweets)
    calculations_by_day = {}

    for day, tweets in tweets_by_day.items():
        calculations_by_day[day] = get_all_calculations(tweets)

    return jsonify(calculations_by_day)


@app.route('/running-gap', methods=['GET'])
@cache.cached(timeout=1 * 60)
def running_gap():
    start = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')

    tweets = fetch_tweets_for_date(start, end)

    return jsonify({
        'longest_gap': get_longest_gap(tweets),
        'current_gap': get_current_gap(tweets)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
