<template>
  <canvas ref="chart" class="chart"></canvas>
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
  LineController,
  LineElement,
} from 'chart.js'

import { fetchSummary } from '../api'

Chart.register(
  BarController,
  LineController,
  CategoryScale,
  LinearScale,
  PointElement,
  BarElement,
  LineElement,
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
  mounted() {
    const ctx = this.$refs.chart.getContext('2d')
    this.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          {
            type: 'bar',
            label: 'Tweets',
            backgroundColor: '#ff4e3a',
            data: [],
            yAxisID: 'a',
            order: 2,
          },
          {
            type: 'bar',
            label: 'Retweets',
            backgroundColor: '#44a58a',
            data: [],
            yAxisID: 'a',
            order: 2,
          },
          {
            type: 'bar',
            label: 'Retweets with comment',
            backgroundColor: '#ffc208',
            data: [],
            yAxisID: 'a',
            order: 2,
          },
          {
            type: 'line',
            label: 'Čas',
            backgroundColor: '#000000',
            borderColor: '#000000',
            data: [],
            yAxisID: 'b',
            order: 1,
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
  methods: {
    async fetch() {
      try {
        this.summary = await fetchSummary()
        this.updateChart()
      } catch (error) {
        console.error(error)
      }
    },
    updateChart() {
      const labels = []
      const tweets = []
      const retweets = []
      const retweetsWithComment = []
      const time = []

      forEach(this.summary, (calculations, date) => {
        labels.push(lightFormat(parseISO(date), 'd. M.'))
        tweets.push(calculations.tweet)
        retweets.push(calculations.retweet)
        retweetsWithComment.push(calculations.retweetWithComment)
        time.push(calculations.time)
      })

      this.chart.data.labels = labels
      this.chart.data.datasets[0].data = tweets
      this.chart.data.datasets[1].data = retweets
      this.chart.data.datasets[2].data = retweetsWithComment
      this.chart.data.datasets[3].data = time
      this.chart.update()
    },
  },
})
</script>

<style scoped>
.chart {
  background: white;
  padding: 2rem 2rem 1rem 1rem;
  margin-top: 5rem;
}
</style>
