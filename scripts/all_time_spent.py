import requests

from dateutil import rrule
from datetime import datetime
import json

from human_time_duration import human_time_duration

a = "2021-01-01"
b = "2021-12-31"
tweets = []

total_seconds = 0
for i, dt in enumerate(
    rrule.rrule(
        rrule.DAILY,
        dtstart=datetime.strptime(a, "%Y-%m-%d"),
        until=datetime.strptime(b, "%Y-%m-%d"),
    )
):
    daily_data = requests.get(f"https://api.twito.djnd.si/{dt.strftime('%Y-%m-%d')}").json()
    tweets += daily_data["tweets"]
    total_seconds += daily_data["calculations"]["time"]
    if i % 10 == 0:
        print(f"Done with {dt}")

with open("tweets.json", "w") as outfile:
    json.dump({"tweets": tweets}, outfile)

print(total_seconds)
print(human_time_duration(total_seconds))
print(len(tweets))
