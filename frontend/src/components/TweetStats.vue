<template>
  <div class="row">
    <div class="column square square-gray">
      <div class="count">{{ tweetCounts.all }}</div>
      tweetov
    </div>
    <div class="column square square-gray">
      <div class="count">{{ tweetTime }}</div>
      preživel na twitterju
    </div>
  </div>
  <div class="row">
    <div class="column square square-green">
      <div class="count">{{ tweetCounts.original }}</div>
      Izvirni tweeti
    </div>
    <div class="column square square-orange">
      <div class="count">{{ tweetCounts.retweets }}</div>
      Retweeti
    </div>
    <div class="column square square-yellow">
      <div class="count">{{ tweetCounts.retweetsWithComment }}</div>
      Retweeti s komentarjem
    </div>
  </div>
</template>

<script>
import { getTweetTime, getTweetCounts } from "../timeAnalysis";
import { fetchTweetData } from "../api";

export default {
  data() {
    return {
      tweets: [],
    };
  },
  computed: {
    tweetCounts() {
      return getTweetCounts(this.tweets);
    },
    tweetTime() {
      return getTweetTime(this.tweets);
    }
  },
  async created() {
    try {
      this.tweets = await fetchTweetData();
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style scoped>

@media (min-width: 768px) {
  .row {
    display: flex;
  }
  .column {
    margin: 0 0.5rem;
    flex: 1;
  }
  .column:first-child { margin-left: 0; }
  .column:last-child { margin-right: 0; }
}

.square {
  margin-bottom: 1rem;
  text-align: center;
  padding: 1rem;
  border-radius: 0.5rem;

}
.square-gray { background: #d8d8d8; }
.square-green { background: #4fe3c1; }
.square-orange { background: #f5a623; }
.square-yellow { background: #f8e71d; }

.count {
  font-size: 2rem;
  font-weight: bold;
}
</style>
