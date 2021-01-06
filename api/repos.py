from datetime import datetime

from models import Tweet
from tweets import get_tweet_id, TWEET_ID
from utils import string_to_int


def map_tweet_to_tweet_dict(tweet):
    twitter_id = get_tweet_id(tweet)
    from_user_created_at = datetime.fromisoformat(tweet.get('from_user_created_at'))
    tweet.pop(from_user_created_at, None)
    tweet.pop(TWEET_ID, None)
    tweet.pop('created_at', None)

    tweet_data = {
        **tweet,
        'twitter_id': twitter_id,
        'favorite_count': string_to_int(tweet.get('favourite_count')),
        'from_user_favourites_count': string_to_int(tweet.get('from_user_favourites_count'), 0),
        'from_user_followercount': string_to_int(tweet.get('from_user_followercount')),
        'from_user_friendcount': string_to_int(tweet.get('from_user_friendcount')),
        'from_user_tweetcount': string_to_int(tweet.get('from_user_tweetcount')),
        'from_user_verified': string_to_int(tweet.get('from_user_verified')),
        'possibly_sensitive': string_to_int(tweet.get('possibly_sensitive')),
        'retweet_count': string_to_int(tweet.get('retweet_count')),
        'time': string_to_int(tweet.get('time')),
        'from_user_created_at': from_user_created_at,
    }

    return tweet_data


def store_tweet(tweet):
    tweet_data = map_tweet_to_tweet_dict(tweet)
    tweet_model = Tweet(**tweet_data)
    return tweet_model.create_or_first()

