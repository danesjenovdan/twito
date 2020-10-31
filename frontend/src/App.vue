<template>
  <div>
    <h1 class="header-text">Maršal Twito - Sledilnik</h1>
    <header class="header-image">
      <img src="./assets/header.jpg" class="header-image" />
    </header>
    <h3 class="tagline">Slepo sledimo, kamorkoli nas že vodi</h3>
    <main class="content">
      <tweet-stats />
    </main>
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
.header-text {
  margin: 0;
  padding: 0.5em;
}

.header-image {
  line-height: 0;
  background: #c54013;
}

.header-image img {
  width: 100%;
  max-width: 960px;
}

.tagline {
  border-bottom: 3px solid black;
  margin: 0;
  padding: 0.5em;
}

.content {
  padding: 1rem;
  max-width: 960px;
  margin: 0 auto;
}
</style>
