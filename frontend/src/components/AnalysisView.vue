<template>
  <div class="mt">
    <big-tweet-counts
      :title-count="$t('summary.averageNumberOfTweets')"
      :title-time="$t('summary.averageTimeEstimation')"
      :count="summary.averageDailyTweetCount"
      :time="summary.averageDailyTweetTime"
    />
    <summary-chart />
  </div>
</template>

<script>
import { defineComponent } from 'vue'

import { fetchAnalysis } from '../api'
import BigTweetCounts from './BigTweetCounts.vue'
import SummaryChart from './SummaryChart.vue'

export default defineComponent({
  components: {
    BigTweetCounts,
    SummaryChart,
  },
  data() {
    return {
      summary: {
        averageDailyTweetCount: 0,
        averageDailyTweetCountDifference: 0,
        averageDailyTweetCountDifferencePercentage: 0,
        averageDailyTweetTime: 0,
        averageDailyTweetTimeDifference: 0,
        averageDailyTweetTimeDifferencePercentage: 0,
      },
    }
  },
  created() {
    this.fetch()
  },
  methods: {
    async fetch() {
      try {
        const response = await fetchAnalysis()
        this.summary = response
      } catch (error) {
        console.error(error)
      }
    },
  },
})
</script>

<style scoped>
.mt {
  margin-top: 3.75rem;
}
</style>