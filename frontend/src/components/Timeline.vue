<template>
  <div class="wrapper">
    <div class="label">razporeditev tvitov čez dan</div>
    <div class="timeline">
      <div
        v-for="tweet in tweetsWithTime"
        :key="tweet.id"
        class="tweet"
        :style="tweet.style"
      ></div>
    </div>
    <div class="legend">
      <div class="hour">00:00</div>
      <div class="hour hidden-mobile">04:00</div>
      <div class="hour">08:00</div>
      <div class="hour hidden-mobile">12:00</div>
      <div class="hour">16:00</div>
      <div class="hour hidden-mobile">20:00</div>
      <div class="hour">00:00</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import startOfDay from 'date-fns/startOfDay'
import { TweetType, Tweet, getTweetType } from '../utils'

const addDistances = (tweets) => {
  if (tweets.length === 0) return []
  const start = startOfDay(new Date(tweets[0].time * 1000))
  const startInSeconds = start.getTime() / 1000
  const secondsInDay = 24 * 60 * 60
  const colorMap = {
    [TweetType.ORIGINAL]: '#ff4e3a',
    [TweetType.RETWEET]: '#44a58a',
    [TweetType.RETWEET_WITH_COMMENT]: '#ffc208',
  }
  return tweets.map((tweet) => ({
    ...tweet,
    style: {
      left: `${((tweet.time - startInSeconds) / secondsInDay) * 100}%`,
      background: colorMap[getTweetType(tweet)],
    },
  }))
}

export default defineComponent({
  props: {
    tweets: { type: Array as PropType<Tweet[]>, default: () => [] },
  },
  computed: {
    tweetsWithTime() {
      return addDistances(this.tweets)
    },
  },
})
</script>

<style scoped>
.wrapper {
  margin-bottom: 1.5rem;
}

.label {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  line-height: 1em;
}

.timeline {
  background: repeating-linear-gradient(
    90deg,
    #f7f7f7,
    #f7f7f7 calc(4.1667% - 1px),
    #afafaf calc(4.1667% - 1px),
    #afafaf 4.1667%
  );
  border: 2px solid #afafaf;
  border-right-width: 1px;
  height: 5.25rem;
  width: 100%;
  position: relative;
  margin-bottom: 0.5rem;
}

.tweet {
  position: absolute;
  width: 2px;
  height: 100%;
  top: 0;
}

.legend {
  display: flex;
  font-size: 0.875rem;
  font-weight: bold;
  justify-content: space-between;
}

.hour {
  width: 2.875rem;
}
.hour:first-child {
  margin-right: -1.4375rem;
}
.hour:last-child {
  margin-left: -1.4375rem;
}
</style>