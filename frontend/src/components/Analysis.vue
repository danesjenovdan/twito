<template>
    <div class="mt">
        <big-tweet-counts
          :title-count="$t('summary.averageNumberOfTweets')"
          :title-time="$t('summary.averageTimeEstimation')"
          :count="summary.averageDailyTweetCount"
          :time="summary.averageDailyTweetTime"
        />
        <!-- 
        :trend-tweets-no="summary.averageDailyTweetCountDifference"
        :trend-tweets-percentage="summary.averageDailyTweetCountDifferencePercentage"
        :trend-time="summary.averageDailyTweetTimeDifferencePercentage"
        :trend-time-percentage="summary.averageDailyTweetTimeDifferencePercentage"
        -->

        <!-- <br />

        <big-tweet-counts
          :title-count="$t('summary.averageNumberOfTweetsPandemic')"
          :title-time="$t('summary.averageTimeEstimationPandemic')"
          :count="summary.averageDailyTweetCountSincePandemic"
          :time="summary.averageDailyTweetTimeSincePandemic"
          :trend-tweets-no="summary.averageDailyTweetCountDifferenceSincePandemic"
          :trend-tweets-percentage="summary.averageDailyTweetCountDifferencePercentageSincePandemic"
          :trend-time="summary.averageDailyTweetTimeDifferencePercentageSincePandemic"
          :trend-time-percentage="summary.averageDailyTweetTimeDifferencePercentageSincePandemic"
        /> -->

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
    SummaryChart
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
        // averageDailyTweetCountSincePandemic: 0,
        // averageDailyTweetCountDifferenceSincePandemic: 0,
        // averageDailyTweetCountDifferencePercentageSincePandemic: 0,
        // averageDailyTweetTimeSincePandemic: 0,
        // averageDailyTweetTimeDifferenceSincePandemic: 0,
        // averageDailyTweetTimeDifferencePercentageSincePandemic: 0,
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