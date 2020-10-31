const API_URL = import.meta.env.VITE_API_URL;

export const fetchTweetData = async () => {
  const response = await fetch(`${API_URL}2020-10-30`);
  if (response.status !== 200) {
    console.log(
      "Looks like there was a problem. Status Code: " + response.status
    );
    return;
  }
  return await response.json();
}
