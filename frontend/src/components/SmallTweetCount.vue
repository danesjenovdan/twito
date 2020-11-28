<template>
  <div class="small-count" :style="colorStyle">
    <div class="small-count-number">{{ count }}</div>
    <div class="small-count-label" v-html="label" />
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
          singular: 'izviren<br>tweet',
          dual: 'izvirna<br>tweeta',
          smallPlural: 'izvirni<br>tweeti',
          bigPlural: 'izvirnih<br>tweetov',
        },
        retweets: {
          singular: '<br>RT',
          dual: '<br>RT-ja',
          smallPlural: '<br>RT-ji',
          bigPlural: '<br>RT-jev',
        },
        retweetsWithComment: {
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
  align-items: flex-end;
  border-width: 0.3125rem;
  border-style: solid;
  display: flex;
  padding: 1rem;
  justify-content: center;
}
.small-count:not(:last-child) {
  margin-bottom: 1rem;
}

.small-count-label {
  margin-left: 0.375rem;
  line-height: 1em;
}

.small-count-number {
  font-size: 3.125rem;
  line-height: 0.76em;
  font-weight: bold;
  height: 2.375rem;
}

@media (min-width: 768px) {
  .small-count {
    margin-bottom: 0 !important;
  }
}
</style>
