<template>
  <div class="row">
    <div class="column big-count tweet-count">
      <div class="big-count-label">število tweetov</div>
      <div class="big-count-number">{{ count }}</div>
    </div>
    <div class="column big-count tweet-time">
      <div class="big-count-label">ocena časa, preživetega na Twitterju</div>
      <div class="big-count-number">
        {{ formattedTime.hours }}<span class="time-unit">h</span>
        {{ formattedTime.minutes }}<span class="time-unit">min</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    count: { type: Number, required: true },
    time: { type: Number, required: true },
  },
  computed: {
    formattedTime() {
      const tweetTimeInMinutes = Math.round(this.time / 60000)

      const hours = Math.floor(tweetTimeInMinutes / 60)
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, '0')

      return { hours, minutes }
    },
  },
})
</script>

<style scoped>
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

@media (min-width: 768px) {
  .big-count {
    margin-bottom: 0;
  }
}
</style>
