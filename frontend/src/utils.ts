import camelCase from 'lodash-es/camelCase'
import mapKeys from 'lodash-es/mapKeys'
import format from 'date-fns/format'
import { sl } from 'date-fns/locale'

export type Tweet = {
  createdAt: string
  id: string
  quotedStatusId: string
  text: string
}

export enum TweetType {
  ORIGINAL,
  RETWEET,
  RETWEET_WITH_COMMENT,
}

const RETWEET_PREFIX = 'RT '
const MAX_TIME_BETWEEN_TWEETS = 5 * 60 * 1000 // 5 minutes
const TIME_FOR_ONE_TWEET = 2 * 60 * 1000 // 2 minutes

// Splits a list of tweets into intervals less than MAX_TIME_BETWEEN_TWEETS apart
const generateIntervals = (tweets: Tweet[]): Tweet[][] => {
  const allSessions = []
  let currentSession = []

  tweets.forEach((tweet) => {
    if (currentSession.length === 0) {
      currentSession.push(tweet)
      return
    }

    const currentTweetTime = getTweetTimestamp(tweet)
    const lastTweetInSession = currentSession[currentSession.length - 1]
    const lastTweetInSessionTime = getTweetTimestamp(lastTweetInSession)

    const timeBetweenTweets = currentTweetTime - lastTweetInSessionTime

    if (timeBetweenTweets > MAX_TIME_BETWEEN_TWEETS) {
      allSessions.push(currentSession)
      currentSession = []
    }
    currentSession.push(tweet)
  })

  if (currentSession.length > 0) {
    allSessions.push(currentSession)
  }

  return allSessions
}

// Sums interval durations to get total tweeting time
export const getTweetTime = (tweets: Tweet[]): number =>
  generateIntervals(tweets).reduce((duration, interval) => {
    const intervalStart = getTweetTimestamp(interval[0])
    const intervalEnd = getTweetTimestamp(interval[interval.length - 1])

    return (
      duration +
      Math.max(
        intervalEnd - intervalStart,
        TIME_FOR_ONE_TWEET // Intervals with just one tweet should return whatever we think it took
      )
    )
  }, 0)

type TweetCounts = {
  all: number
  original: number
  retweets: number
  retweetsWithComment: number
}

// Counts tweets by type
export const getTweetCounts = (tweets: Tweet[]): TweetCounts => {
  return {
    all: tweets.length,
    original: tweets.filter((t) => getTweetType(t) === TweetType.ORIGINAL)
      .length,
    retweets: tweets.filter((t) => getTweetType(t) === TweetType.RETWEET)
      .length,
    retweetsWithComment: tweets.filter(
      (t) => getTweetType(t) === TweetType.RETWEET_WITH_COMMENT
    ).length,
  }
}

// Determines type of tweet
export const getTweetType = (tweet: Tweet): TweetType => {
  if (tweet.text.startsWith(RETWEET_PREFIX)) {
    return TweetType.RETWEET
  } else if (tweet.quotedStatusId) {
    return TweetType.RETWEET_WITH_COMMENT
  } else {
    return TweetType.ORIGINAL
  }
}

// Returns timestamp of tweet
const getTweetTimestamp = (tweet) => new Date(tweet.createdAt).getTime()

// Converts object keys to camelCase
export const keysToCamel = (
  object: Record<string, unknown>
): Record<string, unknown> => mapKeys(object, (_, k) => camelCase(k))

// Formats date a specific way used as title and social media share text
export const formatDate = (dateString: string): string =>
  format(new Date(dateString), 'EEEE, d. MMMM y', { locale: sl })
