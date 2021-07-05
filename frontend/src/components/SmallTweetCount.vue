<template>
  <div class="small-count" :style="colorStyle">
    <div class="small-count-number">{{ count }}</div>
    <div class="small-count-label">{{ label }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

import { TweetType } from '../types.ts'
import { tweetColorStyle, getWordForm } from '../utils.ts'

export default defineComponent({
  props: {
    type: { type: String as PropType<TweetType>, required: true },
    count: { type: Number, required: true },
  },
  computed: {
    label() {
      return getWordForm(this.type, this.count)
    },
    colorStyle() {
      return tweetColorStyle[this.type]
    },
  },
})
</script>

<style scoped>
.small-count {
  border-width: 0.3125rem;
  border-style: solid;
  flex: inherit;
  padding: 1rem 0;
  text-align: center;
  min-width: 20%;
}

.small-count-label {
  line-height: 1em;
  max-width: 6.5rem;
  margin: 0.5rem auto 0;
}

.small-count-number {
  font-size: 3.125rem;
  font-weight: bold;
  height: 2.375rem;
  line-height: 0.76em;
}

@media (min-width: 768px) {
  .small-count {
    align-items: flex-end;
    display: flex;
    justify-content: center;
    padding: 1rem;
    text-align: left;
  }
  .small-count-label {
    flex: 0;
    margin: 0 0 0 0.375rem;
  }
}
</style>
