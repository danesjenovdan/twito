import camelCase from 'lodash-es/camelCase'
import mapKeys from 'lodash-es/mapKeys'
import capitalize from 'lodash-es/capitalize'
import format from 'date-fns/format'
import parseISO from 'date-fns/parseISO'
import { sl, enGB } from 'date-fns/locale'
import { Tweet, TweetType } from './types'

const RETWEET_PREFIX = 'RT '

const WORD_FORMS = {
  si: {
    [TweetType.TWEET]: {
      singular: 'izviren tvit',
      dual: 'izvirna tvita',
      smallPlural: 'izvirni tviti',
      bigPlural: 'izvirnih tvitov',
    },
    [TweetType.RETWEET]: {
      singular: 'RT',
      dual: 'RT‑ja',
      smallPlural: 'RT‑ji',
      bigPlural: 'RT‑jev',
    },
    [TweetType.RETWEET_WITH_COMMENT]: {
      singular: 'RT s komentarjem',
      dual: 'RT‑ja s komentarjem',
      smallPlural: 'RT‑ji s komentarjem',
      bigPlural: 'RT‑jev s komentarjem',
    },
  },
  en: {
    [TweetType.TWEET]: {
      singular: 'original tweet',
      dual: 'original tweets',
      smallPlural: 'original tweets',
      bigPlural: 'original tweets',
    },
    [TweetType.RETWEET]: {
      singular: 'RT',
      dual: 'RTs',
      smallPlural: 'RTs',
      bigPlural: 'RTs',
    },
    [TweetType.RETWEET_WITH_COMMENT]: {
      singular: 'RT with comment',
      dual: 'RTs with comment',
      smallPlural: 'RTs with comment',
      bigPlural: 'RTs with comment',
    },
  },
}

const DATE_FORMATS = {
  en: 'EEEE, d MMMM y',
  si: 'EEEE, d. MMMM y',
}

// Returns Slovenian grammatical number for specified count
const getNumber = (count) => {
  if (count === 1) {
    return 'singular'
  } else if (count === 2) {
    return 'dual'
  } else if (count === 3 || count === 4) {
    return 'smallPlural'
  }
  return 'bigPlural'
}

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
export const keysToCamel = (
  object: Record<string, unknown>
): Record<string, unknown> => mapKeys(object, (_, k) => camelCase(k))

const getLocale = (lang: string) => {
  if (lang === 'en') return enGB
  return sl
}

// Formats date a specific way used as title and social media share text
export const formatDate = (dateString: string, lang = 'si'): string =>
  capitalize(format(parseISO(dateString), DATE_FORMATS[lang], { locale: getLocale(lang) }))

export const formatDateMobile = (dateString: string, lang = 'si'): string =>
  capitalize(format(parseISO(dateString), DATE_FORMATS[lang], { locale: getLocale(lang) }))

// Calculates hours and minutes from seconds
export const formatSeconds = (
  seconds: number
): { hours: number; minutes: number } => {
  const tweetTimeInMinutes = Math.round(seconds / 60)

  const hours = Math.floor(tweetTimeInMinutes / 60)
  const minutes = tweetTimeInMinutes % 60

  return { hours, minutes }
}

// Border and background colors for different tweet types
export const tweetColorStyle = {
  [TweetType.TWEET]: {
    backgroundColor: '#ffedeb',
    borderColor: '#ff4e3a',
  },
  [TweetType.RETWEET]: {
    backgroundColor: '#ecf6f3',
    borderColor: '#44a58a',
  },
  [TweetType.RETWEET_WITH_COMMENT]: {
    backgroundColor: '#fff9e6',
    borderColor: '#ffc208',
  },
}

// Returns Slovenian word form for specified count and tweet type
export const getWordForm = (type: TweetType, count: number, lang = 'si'): string => {
  const number = getNumber(count % 100)
  return WORD_FORMS[lang][type][number]
}
