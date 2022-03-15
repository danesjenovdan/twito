import mapValues from 'lodash-es/mapValues'
import { keysToCamel } from './utils'
import { GapResponse, SingleDateResponse, SummaryResponse, AnalysisResponse } from './types'

const API_URL = import.meta.env.VITE_API_URL

export const fetchSingleDate = async (
  date: string
): Promise<SingleDateResponse> => {
  const response = await fetch(API_URL + date)
  if (response.status !== 200) {
    console.log(
      'Looks like there was a problem. Status Code: ' + response.status
    )
    return
  }

  const responseData = await response.json()
  return {
    calculations: keysToCamel(responseData.calculations),
    tweets: responseData.tweets.map(keysToCamel),
    hashtags: responseData.hashtags,
    startOfDay: responseData.start_of_day,
    trendTweetsNo: responseData.trendTweetsNo,
    trendTweetsPercentage: responseData.trendTweetsPercentage,
    trendTime: responseData.trendTime,
    trendTimePercentage: responseData.trendTimePercentage,
    domains: responseData.domains,
    retweets: responseData.retweeted_users
  } as SingleDateResponse
}

export const fetchGap = async (): Promise<GapResponse> => {
  const response = await fetch(`${API_URL}running-gap`)
  if (response.status !== 200) {
    console.log(
      `Looks like there was a problem. Status Code: ${response.status}`
    )
    return
  }

  const responseData = await response.json()
  return keysToCamel(responseData) as GapResponse
}

export const fetchSummary = async (): Promise<SummaryResponse> => {
  const response = await fetch(API_URL + 'summary')
  if (response.status !== 200) {
    console.log(
      'Looks like there was a problem. Status Code: ' + response.status
    )
    return
  }

  const responseData = await response.json()
  return mapValues(responseData, keysToCamel) as SummaryResponse
}

export const fetchAnalysis = async (): Promise<AnalysisResponse> => {
  const response = await fetch(`${API_URL}fetch-analysis`)
  if (response.status !== 200) {
    console.log(
      `Looks like there was a problem. Status Code: ${response.status}`
    )
    return
  }

  const responseData = await response.json()

  return {
    averageDailyTweetCount: responseData.avg_tweet_summary,
    averageDailyTweetCountDifference: responseData.avg_tweets_trend,
    averageDailyTweetCountDifferencePercentage: responseData.avg_tweets_trend_percentage,
    averageDailyTweetTime: responseData.avg_time_summary,
    averageDailyTweetTimeDifference: responseData.avg_time_summary_trend,
    averageDailyTweetTimeDifferencePercentage: responseData.avg_time_summary_trend_percentage,
    // averageDailyTweetCountSincePandemic: responseData.avg_tweet_summary_pandemic,
    // averageDailyTweetCountDifferenceSincePandemic: responseData.avg_tweets_trend_since_pandemic,
    // averageDailyTweetCountDifferencePercentageSincePandemic: responseData.avg_tweets_trend_since_pandemic_percentage,
    // averageDailyTweetTimeSincePandemic: responseData.avg_time_summary_pandemic,
    // averageDailyTweetTimeDifferenceSincePandemic: responseData.avg_time_trend_since_pandemic,
    // averageDailyTweetTimeDifferencePercentageSincePandemic: responseData.avg_time_trend_since_pandemic_percentage,
  } as AnalysisResponse;
} 
