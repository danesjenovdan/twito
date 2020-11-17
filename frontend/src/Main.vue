<template>
  <div class="container">
    <header class="header-image">Tu not bo žumer nekaj carskega narisau</header>
    <tweet-stats v-for="d in dates" :key="d" :date="d" />
    <div ref="bottom" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import subDays from 'date-fns/subDays'
import formatISO from 'date-fns/formatISO'
import throttle from 'lodash-es/throttle'
import TweetStats from './components/TweetStats.vue'

const getShortIsoDate = (date) => formatISO(date, { representation: 'date' })

export default defineComponent({
  components: {
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
        threshold: 1,
      }

      const addDayThrottled = throttle(this.addDay, 1000, { trailing: false })
      const observer = new IntersectionObserver(addDayThrottled, options)
      observer.observe(this.$refs.bottom)
    },
  },
})
</script>

<style scoped>
.container {
  max-width: 1280px;
  margin: 0 auto;
}

.header-image {
  line-height: 0;
  background: #44a58a;
  padding: 25% 0;
}
</style>
