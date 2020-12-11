import { Tweet, keysToCamel } from './utils'

const API_URL = import.meta.env.VITE_API_URL

type SingleDateResponse = {
  calculations: {
    tweet: number
    retweet: number
    retweetWithComment: number
    time: number
  }
  tweets: Tweet[]
}

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

export const fetchGap = async (): Promise<Number> => {
  const response = await fetch(`${API_URL}running-gap`);
  if (response.status !== 200) {
    console.log(
      `Looks like there was a problem. Status Code: ${response.status}`
    );
    return
  }

  const responseData = await response.text();
  return parseInt(responseData, 10);
};
