<template>
  <div class="container">
    <header class="header-image">
      Tu not bo žumer nekaj carskega narisau
    </header>
    <tweet-stats />
  </div>
</template>

<script>
import TweetStats from "./components/TweetStats.vue";

export default {
  components: {
    TweetStats,
  },
};
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
