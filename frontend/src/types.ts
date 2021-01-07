export type Tweet = {
  createdAt: string
  id: string
  quotedStatusId: string
  text: string
}

export enum TweetType {
  TWEET = 'tweet',
  RETWEET = 'retweet',
  RETWEET_WITH_COMMENT = 'retweetWithComment',
}

export type TweetStyle = {
  backgroundColor: string
  borderColor: string
}

export type Hashtag = {
  hashtag: string
  number: number
}

export type Calculation = {
  tweet: number
  retweet: number
  retweetWithComment: number
  time: number
}

export type SingleDateResponse = {
  calculations: Calculation
  tweets: Tweet[]
  hashtags: Hashtag[]
  startOfDay: string
}

export type GapResponse = {
  longestGap: number
  currentGap: number
}

export type SummaryResponse = Record<string, Calculation>
