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

export type Hashtag = {
  hashtag: string
  number: number
}

export type Calculation = {
  tweet: number
  retweet: number
  retweetWithComment: number
  time: number
  hashtags: Hashtag[]
}

export type SingleDateResponse = {
  calculations: Calculation
  tweets: Tweet[]
}

export type GapResponse = {
  longestGap: number
  currentGap: number
}

export type SummaryResponse = Record<string, Calculation>
