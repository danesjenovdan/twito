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
  longest_gap: number
  current_gap: number
}

export type SummaryResponse = Record<string, Calculation>
