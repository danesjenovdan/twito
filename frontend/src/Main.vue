<template>
  <div class="container">
    <header class="header-image">Tu not bo žumer nekaj carskega narisau</header>
    <tweet-stats :date="date" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import TweetStats from './components/TweetStats.vue'

export default defineComponent({
  components: {
    TweetStats,
  },
  props: {
    date: {
      type: String,
      default() {
        return new Date().toISOString()
      },
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
