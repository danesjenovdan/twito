<template>
  <div class="small-count" :style="colorStyle">
    <div class="small-count-number">{{ count }}</div>
    <div class="small-count-label" v-html="label" />
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'

import { TweetType } from '../types.ts'

export default defineComponent({
  props: {
    type: { type: String as PropType<TweetType>, required: true },
    count: { type: Number, required: true },
  },
  computed: {
    label() {
      const WORD_FORMS = {
        [TweetType.TWEET]: {
          singular: 'izviren<br>tvit',
          dual: 'izvirna<br>tvita',
          smallPlural: 'izvirni<br>tviti',
          bigPlural: 'izvirnih<br>tvitov',
        },
        [TweetType.RETWEET]: {
          singular: '<br>RT',
          dual: '<br>RT-ja',
          smallPlural: '<br>RT-ji',
          bigPlural: '<br>RT-jev',
        },
        [TweetType.RETWEET_WITH_COMMENT]: {
          singular: 'RT s<br>komentarjem',
          dual: 'RT-ja s<br>komentarjem',
          smallPlural: 'RT-ji s<br>komentarjem',
          bigPlural: 'RT-jev s<br>komentarjem',
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
      return {
        tweet: {
          backgroundColor: '#ffedeb',
          borderColor: '#ff4e3a',
        },
        retweet: {
          backgroundColor: '#ecf6f3',
          borderColor: '#44a58a',
        },
        retweetWithComment: {
          backgroundColor: '#fff9e6',
          borderColor: '#ffc208',
        },
      }[this.type]
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
  margin-left: 0.375rem;
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
}
</style>
