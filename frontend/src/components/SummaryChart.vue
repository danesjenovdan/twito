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

import { fetchSummary } from '../api'

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
  mounted() {
    const ctx = this.$refs.chart.getContext('2d')
    this.chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: [],
        datasets: [
          {
            label: 'Tweets',
            backgroundColor: '#ff4e3a',
            data: [],
          },
          {
            label: 'Retweets with comment',
            backgroundColor: '#ffc208',
            data: [],
          },
          {
            label: 'Retweets',
            backgroundColor: '#44a58a',
            data: [],
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

      forEach(this.summary, (calculations, date) => {
        labels.push(lightFormat(parseISO(date), 'd. M.'))
        tweets.push(calculations.tweet)
        retweets.push(calculations.retweet)
        retweetsWithComment.push(calculations.retweetWithComment)
      })

      this.chart.data.labels = labels
      this.chart.data.datasets[0].data = tweets
      this.chart.data.datasets[0].label = 'Izvirnih tvitov'
      this.chart.data.datasets[1].data = retweetsWithComment
      this.chart.data.datasets[1].label = 'RT s komentarjem'
      this.chart.data.datasets[2].data = retweets
      this.chart.data.datasets[2].label = 'RT-jev'
      this.chart.update()
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