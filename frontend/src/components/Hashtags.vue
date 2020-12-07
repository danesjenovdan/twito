<template>
  <div class="wrapper">
    <div class="label">Najbolj uporabljeni hashtagi</div>
    <div class="hashtagContainer">
      <div v-for="hashtag in topHashtags" :key="hashtag" class="hashtag">
        {{ hashtag }}
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    hashtags: { type: Object, default: () => ({}), required: true },
  },
  computed: {
    topHashtags() {
      return Object.entries(this.hashtags)
        .slice(0, 5)
        .map(
          ([hashtag, number], index) =>
            `${index + 1}. ${hashtag}: ${number}-krat`
        )
    },
  },
})
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;

  margin: 1.5rem 0;
}
.label {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  line-height: 1em;
}
.hashtag {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}
</style>
