<template>
  <div>
    <div class="box-top">{{ $t('summary.title') }}</div>
    <div class="frame">
      <canvas ref="chart" class="chart"></canvas>
      <div class="legend">
        <div
          v-for="(style, type) in tweetColorStyle"
          :key="type"
          :style="style"
          class="legend-item"
        >
          {{ getWordForm(type, 3, $i18n.locale) }}
        </div>
      </div>
    </div>
    <div class="box-bottom button-container">
      <share-buttons />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import forEach from 'lodash-es/forEach'
import parseISO from 'date-fns/parseISO'
import lightFormat from 'date-fns/lightFormat'
import {
  Chart,
  BarController,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  Tooltip,
} from 'chart.js'
import ShareButtons from './ShareButtons.vue'

import { fetchSummary } from '../api'
import { TweetType } from '../types'
import { formatDateMobile, tweetColorStyle, getWordForm } from '../utils'

Chart.register(
  BarController,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  Tooltip
)

Chart.defaults.font.family = '"Space Grotesk", sans-serif'
Chart.defaults.font.size = 14

export default defineComponent({
  components: {
    ShareButtons
  },
  data() {
    return {
      chart: {},
      summary: {},
      tweetColorStyle,
      getWordForm,
    }
  },
  created() {
    this.fetch()
  },
  methods: {
    async fetch() {
      try {
        this.summary = await fetchSummary()
        this.generateChart()
      } catch (error) {
        console.error(error)
      }
    },
    generateChart() {
      const labels = []
      const tooltipTitles = []
      const tweets = []
      const retweets = []
      const retweetsWithComment = []

      forEach(this.summary, (calculations, date) => {
        labels.push(lightFormat(parseISO(date), 'd. M.'))
        tooltipTitles.push(formatDateMobile(date))
        tweets.push(calculations.tweet)
        retweets.push(calculations.retweet)
        retweetsWithComment.push(calculations.retweetWithComment)
      })

      const ctx = this.$refs.chart.getContext('2d')
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: getWordForm(TweetType.TWEET, 5, this.$i18n.locale),
              backgroundColor: '#ff4e3a',
              data: tweets,
            },
            {
              label: getWordForm(TweetType.RETWEET_WITH_COMMENT, 5, this.$i18n.locale),
              backgroundColor: '#ffc208',
              data: retweetsWithComment,
            },
            {
              label: getWordForm(TweetType.RETWEET, 5, this.$i18n.locale),
              backgroundColor: '#44a58a',
              data: retweets,
            },
          ],
        },
        options: {
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true,
            },
          },
        },
      })
    },
  },
})
</script>

<style scoped>
.chart {
  background: white;
  padding: 1rem 1rem 0 0;
}

/* .legend {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
} */

.legend-item {
  border-width: 0.3125rem;
  border-style: solid;
  display: flex;
  font-size: 1rem;
  align-items: center;
  justify-content: center;
  height: 3rem;
  margin: 0.75rem 0 0;
}

@media (min-width: 768px) {
  .legend {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
  }

  .legend-item {
    font-size: 0.8125rem;
    width: 10.5rem;
    margin: 0 0.75rem 0 0;
  }

  .legend-item:last-child {
    margin: 0;
  }
}
</style>
