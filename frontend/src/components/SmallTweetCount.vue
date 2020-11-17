<template>
  <div class="small-count" :style="colorStyle">
    <div class="small-count-number">{{ count }}</div>
    <div class="small-count-label">{{ label }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    type: { type: String, required: true },
    count: { type: Number, required: true },
  },
  computed: {
    label() {
      const WORD_FORMS = {
        original: {
          singular: 'izviren tweet',
          dual: 'izvirna tweeta',
          smallPlural: 'izvirni tweeti',
          bigPlural: 'izvirnih tweetov',
        },
        retweets: {
          singular: 'RT',
          dual: 'RT-ja',
          smallPlural: 'RT-ji',
          bigPlural: 'RT-jev',
        },
        retweetsWithComment: {
          singular: 'RT s komentarjem',
          dual: 'RT-ja s komentarjem',
          smallPlural: 'RT-ji s komentarjem',
          bigPlural: 'RT-jev s komentarjem',
        },
      }
      const getWordForm = (count) => {
        count = count % 100
        if (count <= 1) {
          return 'singular'
        } else if (count === 2) {
          return 'dual'
        } else if (count < 5) {
          return 'smallPlural'
        }
        return 'bigPlural'
      }
      return WORD_FORMS[this.type][getWordForm(this.count)]
    },
    colorStyle() {
      return {
        original: {
          backgroundColor: '#ffedeb',
          borderColor: '#ff4e3a',
        },
        retweets: {
          backgroundColor: '#ecf6f3',
          borderColor: '#44a58a',
        },
        retweetsWithComment: {
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
  align-items: baseline;
  border-width: 0.3125rem;
  border-style: solid;
  display: flex;
  padding: 1rem;
}

.small-count-label {
  margin-left: 0.5rem;
}

.small-count-number {
  font-size: 4.375rem;
  line-height: 1em;
  font-weight: bold;
  height: 4.375rem;
}
</style>
