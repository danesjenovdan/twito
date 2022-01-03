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
    // TODO: change according to API data
    trendTweetsNo: 5,
    trendTweetsPercentage: 10,
    trendTime: -3876,
    trendTimePercentage: -5,
    domains: [
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
    ],
    retweets: [
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
      { tag: 'Blabla', number: 10 },
    ]
    // ---------------------------------
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
  // TODO: add API call
  return {
    averageDailyTweetCount: 45,
    averageDailyTweetCountDifference: 5,
    averageDailyTweetCountDifferencePercentage: 5,
    averageDailyTweetTime: 10576,
    averageDailyTweetTimeDifference: -1000,
    averageDailyTweetTimeDifferencePercentage: -5,
    averageDailyTweetCountSincePandemic: 45,
    averageDailyTweetCountDifferenceSincePandemic: 5,
    averageDailyTweetCountDifferencePercentageSincePandemic: 5,
    averageDailyTweetTimeSincePandemic: 10576,
    averageDailyTweetTimeDifferenceSincePandemic: -1000,
    averageDailyTweetTimeDifferencePercentageSincePandemic: -5,
  } as AnalysisResponse;
} 
