<template>
  <div class="container">
    <ViewButtons></ViewButtons>
    <tweet-stats v-for="d in dates" :key="d" :date="d" />
    <div ref="bottom" />
    <footer-links />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import subDays from 'date-fns/subDays'
import formatISO from 'date-fns/formatISO'
import parseISO from 'date-fns/parseISO'

import FooterLinks from './FooterLinks.vue'
import TweetStats from './TweetStats.vue'
import ViewButtons from './ViewButtons.vue'

const getShortIsoDate = (date) => formatISO(date, { representation: 'date' })

export default defineComponent({
  components: {
    FooterLinks,
    TweetStats,
    ViewButtons,
  },
  provide: {
    inProduction: window.location.hostname === 'twito.si',
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
      isIntersecting: false,
    }
  },
  computed: {
    dateInUrl() {
      return Boolean(this.$route.params.date)
    },
  },
  mounted() {
    if (!this.dateInUrl) {
      this.initInfiniteLoading()
    }
  },
  methods: {
    addDay() {
      const lastDay = parseISO(this.dates[this.dates.length - 1])
      const dayToAdd = getShortIsoDate(subDays(lastDay, 1))
      this.dates = [...this.dates, dayToAdd]
    },
    initInfiniteLoading() {
      const options = {
        root: null,
        rootMargin: '0px 0px 10% 0px',
        threshold: 0,
      }

      const callback = (entries) => {
        entries.forEach((entry) => {
          if (!this.isIntersecting && entry.isIntersecting) {
            this.addDay()
            this.$nextTick(() => {
              this.isIntersecting = false
            })
          }
        })
      }

      const observer = new IntersectionObserver(callback, options)
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
</style>