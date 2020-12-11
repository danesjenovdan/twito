<template>
  <div class="row frame">
    <div class="column big-count tweet-time gap-time">
      <div class="big-count-label">
        najdaljši premor od Twitterja v zadnjih 24 urah
      </div>
      <div class="big-count-number">
        {{ formattedTime.hours }}<span class="time-unit">h</span>
        {{ formattedTime.minutes }}<span class="time-unit">min</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { fetchGap } from '../api';

export default defineComponent({
  data() {
    return {
      gap: 24 * 60 * 60,
    };
  },
  async mounted() {
    this.gap = await fetchGap();
  },
  computed: {
    formattedTime() {
      const tweetTimeInMinutes = Math.round(this.gap / 60)

      const hours = Math.floor(tweetTimeInMinutes / 60)
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, '0')

      return { hours, minutes }
    },
  },
})
</script>

<style scoped>
.frame {
  background: white;
  color: black;
  padding: 2rem 1.75rem;
  text-align: left;
}

.big-count {
  padding: 1.25rem;
  margin-bottom: 1rem;
}

.big-count-label {
  font-size: 1.25rem;
  line-height: 1em;
  padding-bottom: 0.8125rem;
  border-bottom: 1px solid black;
  margin-bottom: 1.1875rem;
  font-weight: bold;
}

.big-count-number {
  font-size: 3rem;
  line-height: 0.725em;
  font-weight: bold;
  height: 0.725em;
}

.time-unit {
  font-size: 0.5em;
}

.tweet-count {
  background: #ddf7f8;
}

.tweet-time {
  background: #ffeacc;
  flex: 2;
}

.gap-time {
  color: #000000;
  text-align: left;
}

@media (min-width: 768px) {
  .big-count {
    margin-bottom: 0;
  }
}
</style>
