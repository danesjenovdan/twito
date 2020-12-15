<template>
  <div class="small-count" :style="colorStyle">
    <div class="small-count-number">{{ count }}</div>
    <div class="small-count-label">{{ label }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

import { TweetType } from '../types.ts'
import { tweetColorStyle } from '../utils.ts'

export default defineComponent({
  props: {
    type: { type: String as PropType<TweetType>, required: true },
    count: { type: Number, required: true },
  },
  computed: {
    label() {
      const WORD_FORMS = {
        [TweetType.TWEET]: {
          singular: 'izviren tvit',
          dual: 'izvirna tvita',
          smallPlural: 'izvirni tviti',
          bigPlural: 'izvirnih tvitov',
        },
        [TweetType.RETWEET]: {
          singular: 'RT',
          dual: 'RT‑ja',
          smallPlural: 'RT‑ji',
          bigPlural: 'RT‑jev',
        },
        [TweetType.RETWEET_WITH_COMMENT]: {
          singular: 'RT s komentarjem',
          dual: 'RT‑ja s komentarjem',
          smallPlural: 'RT‑ji s komentarjem',
          bigPlural: 'RT‑jev s komentarjem',
        },
      }
      const getWordForm = (count) => {
        count = count % 100
        if (count === 1) {
          return 'singular'
        } else if (count === 2) {
          return 'dual'
        } else if (count === 3 || count === 4) {
          return 'smallPlural'
        }
        return 'bigPlural'
      }
      return WORD_FORMS[this.type][getWordForm(this.count)]
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
  flex: 1;
  padding: 1rem 0;
  text-align: center;
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
