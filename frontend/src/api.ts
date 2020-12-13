import mapValues from 'lodash-es/mapValues'
import { keysToCamel } from './utils'
import { GapResponse, SingleDateResponse, SummaryResponse } from './types'

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
  return responseData
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
