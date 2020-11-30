<template>
  <div class="container">
    <a href="/"><header class="header-image"></header></a>
    <tweet-stats v-for="d in dates" :key="d" :date="d" />
    <div ref="bottom" class="infinite-loading-trigger" />
    <footer-links />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import subDays from 'date-fns/subDays'
import formatISO from 'date-fns/formatISO'
import throttle from 'lodash-es/throttle'

import FooterLinks from './components/FooterLinks.vue'
import TweetStats from './components/TweetStats.vue'

const getShortIsoDate = (date) => formatISO(date, { representation: 'date' })

export default defineComponent({
  components: {
    FooterLinks,
    TweetStats,
  },
  props: {
    date: {
      type: String,
      default: () => getShortIsoDate(new Date()),
    },
  },
  data() {
    return {
      dates: [this.date],
    }
  },
  mounted() {
    if (!this.$route.params.date) {
      this.initInfiniteLoading()
    }
  },
  methods: {
    addDay() {
      const lastDay = new Date(this.dates[this.dates.length - 1])
      const dayToAdd = getShortIsoDate(subDays(lastDay, 1))
      this.dates = [...this.dates, dayToAdd]
    },
    initInfiniteLoading() {
      const options = {
        root: document,
        rootMargin: '0px',
        threshold: 0.75,
      }

      const addDayThrottled = throttle(this.addDay, 250, { trailing: false })
      const observer = new IntersectionObserver(addDayThrottled, options)
      observer.observe(this.$refs.bottom)
    },
  },
})
</script>

<style scoped>
.container {
  max-width: 978px;
  margin: 0 auto;
}

.header-image {
  line-height: 0;
  background: #44a58a;
  padding: 28.15% 0;
  background-image: url('/twito.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.infinite-loading-trigger {
  height: 0.5rem;
}
</style>
