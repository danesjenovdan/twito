import { Tweet, keysToCamel } from './utils'

const API_URL = import.meta.env.VITE_API_URL

export const fetchTweetData = async (date: string): Promise<Tweet[]> => {
  const response = await fetch(API_URL + date)
  if (response.status !== 200) {
    console.log(
      'Looks like there was a problem. Status Code: ' + response.status
    )
    return
  }

  const responseData = await response.json()
  return responseData.map(keysToCamel)
}
