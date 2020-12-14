<template>
  <div class="box-top">Preteklih 90 dni</div>
  <div class="frame">
    <canvas ref="chart" class="chart"></canvas>
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
import { formatDateMobile } from '../utils'

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
  data() {
    return {
      chart: {},
      summary: {},
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
              label: 'Izvirnih tvitov',
              backgroundColor: '#ff4e3a',
              data: tweets,
            },
            {
              label: 'RT-jev s komentarjem',
              backgroundColor: '#ffc208',
              data: retweetsWithComment,
            },
            {
              label: 'RT-jev',
              backgroundColor: '#44a58a',
              data: retweets,
            },
          ],
        },
        options: {
          plugins: {
            annotation: {
              annotations: [
                {
                  type: 'line',
                  mode: 'vertical',
                  scaleID: 'x',
                  value: '1. 12.',
                  borderColor: 'black',
                  borderWidth: 1,
                  label: {
                    backgroundColor: 'rgba(255, 255, 255, 0.66)',
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
                    xAdjust: 15,
                    yAdjust: 60,
                    enabled: true,
                    content: 'Tonin posreduje',
                    rotation: -90,
                  },
                },
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
</style>
