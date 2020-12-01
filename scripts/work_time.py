import requests
from datetime import datetime, timedelta

start_date = datetime.strptime('2020-9-01', '%Y-%m-%d')
number_of_days = 61

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_hour_from_tweet(tweet):
    return tweet['created_at'].split(' ')[-1].split(':')[0]

def count_work_time_tweets(tweets_by_hour):
    return sum([tweets_by_hour[str(hour)] for hour in range(9, 16)])

ratios = []
for day in (start_date + timedelta(days=n) for n in range(number_of_days)):
    tweets = requests.get(f'https://api.twito.si/{day.strftime("%Y-%m-%d")}').json()
    total_number_of_tweets = len(tweets)
    tweets_by_hour = {}
    for hour in range(24):
        relevant_tweets = list(filter(lambda tweet: get_hour_from_tweet(tweet) == str(hour), tweets))
        tweets_by_hour[str(hour)] = len(relevant_tweets)
    
    work_time_tweets = count_work_time_tweets(tweets_by_hour)

    print(day)
    print(f'Total number of tweets {total_number_of_tweets}')
    print(f'Worktime tweets {work_time_tweets}')
    print(f'Freetime tweets {total_number_of_tweets - work_time_tweets}')
    print(f'Ratio of tweets at work {work_time_tweets/total_number_of_tweets}')

    ratios.append(work_time_tweets/total_number_of_tweets)

print('AVERAGE RATIO')
print(sum(ratios) / len(ratios))
