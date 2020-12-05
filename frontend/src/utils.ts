import camelCase from 'lodash-es/camelCase'
import mapKeys from 'lodash-es/mapKeys'
import capitalize from 'lodash-es/capitalize'
import format from 'date-fns/format'
import parseISO from 'date-fns/parseISO'
import { sl } from 'date-fns/locale'

export type Tweet = {
  createdAt: string
  id: string
  quotedStatusId: string
  text: string
}

export enum TweetType {
  TWEET,
  RETWEET,
  RETWEET_WITH_COMMENT,
}

const RETWEET_PREFIX = 'RT '

// Determines type of tweet
export const getTweetType = (tweet: Tweet): TweetType => {
  if (tweet.text.startsWith(RETWEET_PREFIX)) {
    return TweetType.RETWEET
  } else if (tweet.quotedStatusId) {
    return TweetType.RETWEET_WITH_COMMENT
  } else {
    return TweetType.TWEET
  }
}

// Converts object keys to camelCase
export const keysToCamel = (object) => mapKeys(object, (_, k) => camelCase(k))

// Formats date a specific way used as title and social media share text
export const formatDate = (dateString: string): string =>
  capitalize(format(parseISO(dateString), 'EEEE, d. MMMM y', { locale: sl }))

export const formatDateMobile = (dateString: string): string =>
  capitalize(format(parseISO(dateString), 'EEEE, d. M. y', { locale: sl }))
