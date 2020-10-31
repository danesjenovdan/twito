<template>
  <div>{{ tweets }}</div>
</template>

<script>
import { generateIntervals, calculateTweetTime } from "../timeAnalysis";
import {fetchTweetData} from '../api'

export default {
  data() {
    return {
      tweets: [],
    };
  },
  async created() {
    try {
      this.tweets = await fetchTweetData();
    } catch (error) {
      console.error(error);
    }
  },
}
</script>
