<template>
  <div class="wrapper">
    <div class="container">
      <tweet-stats :date="date" :today="date" />
    </div>
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
  props: {
    date: {
      type: String,
      default: () => getShortIsoDate(new Date()),
    },
  },
  data() {
    return {}
  },
})
</script>


<style scoped>
.wrapper {
  overflow-x: hidden;
  background-color: white;
}

.container {
  max-width: 978px;
  margin: 30px auto;
}

.container >>> .box-top,
.container >>> .box-bottom {
  display: none;
}
</style>