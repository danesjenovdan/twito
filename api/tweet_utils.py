def count_tweets_by_type(tweets):
    retweets = [tweet for tweet in tweets if tweet['text'][:2] == 'RT']
    quoted_tweets = [tweet for tweet in tweets if 'RT' in tweet['text'] and tweet not in retweets]
    original_tweets = [tweet for tweet in tweets if tweet not in (retweets + quoted_tweets)]
    
    return {
        'number_of_retweets': len(retweets),
        'number_of_quoted_tweets': len(quoted_tweets),
        'number_of_original_tweets': len(original_tweets)
    }
