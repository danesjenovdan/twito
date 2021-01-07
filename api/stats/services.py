from stats.models import DailySums
from dmi_tcat import fetch_tweets_for_date_string
from slovenian_time import now, start_of_day, end_of_day

def save_daily_sums(date=now().date()):
    
