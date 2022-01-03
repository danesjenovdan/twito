<template>
    <div>
        <tweet-stats v-for="d in dates" :key="d" :date="d" />
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import formatISO from 'date-fns/formatISO'

import TweetStats from './TweetStats.vue'

const getShortIsoDate = (date) => formatISO(date, { representation: 'date' })

export default defineComponent({
  components: {
    TweetStats,
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
})
</script>