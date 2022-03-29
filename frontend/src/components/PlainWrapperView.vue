<template>
  <div class="container">
    <tweet-stats :date="date" :today="date" />
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
.container {
  background-color: white;
  padding: 10px;
}

.container >>> .box-top,
.container >>> .box-bottom {
  display: none;
}

.container >>> .frame {
  padding: 0;
}

.container >>> .wrapper {
  margin: 0;
}
</style>