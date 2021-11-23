<template>
  <div class="container">
    <ViewButtons></ViewButtons>
    <a href="/"><header class="header-image"></header></a>
    <running-gap />
    <summary-chart v-if="!dateInUrl" />
    <div v-if="dateInUrl">
      <tweet-stats v-for="d in dates" :key="d" :date="d" />
    </div>
    <div ref="bottom" />
    <footer-links />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import formatISO from 'date-fns/formatISO'

import FooterLinks from './components/FooterLinks.vue'
import SummaryChart from './components/SummaryChart.vue'
import TweetStats from './components/TweetStats.vue'
import RunningGap from './components/RunningGap.vue'
import ViewButtons from './components/ViewButtons.vue'

const getShortIsoDate = (date) => formatISO(date, { representation: 'date' })

export default defineComponent({
  components: {
    FooterLinks,
    SummaryChart,
    TweetStats,
    RunningGap,
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
})
</script>

<style scoped>
.container {
  max-width: 978px;
  margin: 0 auto;
  margin-bottom: 60px;
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
</style>
