<template>
  <div class="box-top">Preteklih 90 dni</div>
  <div class="frame">
    <canvas ref="chart" class="chart"></canvas>
    <div class="legend">
      <div
        v-for="(style, type) in tweetColorStyle"
        :key="type"
        :style="style"
        class="legend-item"
      >
        {{ getWordForm(type, 3) }}
      </div>
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
import 'chartjs-plugin-annotation/src/index'

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

const getAnnotation = (label, value) => ({
  type: 'line',
  mode: 'vertical',
  scaleID: 'x',
  value,
  borderColor: 'black',
  borderWidth: 1,
  borderDash: [4, 4],
  label: {
    cornerRadius: 0,
    backgroundColor: '#ddf7f8',
    font: {
      // Font family of text, inherits from global
      family: 'Space Grotesk',

      // Font size of text, inherits from global
      size: 14,

      // Font style of text, default below
      style: 'normal',

      // Font color of text, default below
      color: 'black',
    },

    yPadding: 8,
    xPadding: 8,
    position: 'top',
    yAdjust: 15,
    enabled: true,
    content: label,
  },
})

export default defineComponent({
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
              label: getWordForm(TweetType.TWEET, 5),
              backgroundColor: '#ff4e3a',
              data: tweets,
            },
            {
              label: getWordForm(TweetType.RETWEET_WITH_COMMENT, 5),
              backgroundColor: '#ffc208',
              data: retweetsWithComment,
            },
            {
              label: getWordForm(TweetType.RETWEET_WITH_COMMENT, 5),
              backgroundColor: '#44a58a',
              data: retweets,
            },
          ],
        },
        options: {
          plugins: {
            annotation: {
              annotations: [
                getAnnotation('Tonin posreduje    ', '9. 12.'),
                getAnnotation('Razglasitev epidemije', '19. 10.'),
              ],
            },
            tooltip: {
              callbacks: {
                title: (context) => tooltipTitles[context[0].dataIndex],
              },
            },
          },
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
