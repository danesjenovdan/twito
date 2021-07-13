<template>
  <div class="row frame">
    <div class="column big-count tweet-time gap-time">
      <div class="big-count-label">{{ $t('header.noActivity') }}</div>
      <div class="big-count-number">
        <span v-if="currentGap.hours > 0"
          >{{ currentGap.hours }}<span class="time-unit">h</span></span
        >
        {{ currentGap.minutes }}<span class="time-unit">min</span>
      </div>
    </div>
    <div class="column big-count tweet-time gap-time">
      <div class="big-count-label">{{ $t('header.longestBreak') }}</div>
      <div class="big-count-number">
        {{ longestGap.hours }}<span class="time-unit">h</span>
        {{ longestGap.minutes }}<span class="time-unit">min</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { fetchGap } from '../api'
import { formatSeconds } from '../utils'

export default defineComponent({
  data() {
    return {
      longestGap: {
        hours: 0,
        minutes: 0,
      },
      currentGap: {
        hours: 0,
        minutes: 0,
      },
    }
  },
  async mounted() {
    const gaps = await fetchGap()
    this.longestGap = formatSeconds(gaps.longestGap)
    this.currentGap = formatSeconds(gaps.currentGap)
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
  font-size: 5rem;
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
