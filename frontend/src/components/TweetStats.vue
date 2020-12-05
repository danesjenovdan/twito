<template>
  <div class="box-top">
    <a :href="`/${date}`">
      <span class="hidden-mobile">
        {{ formattedDateDesktop }}
      </span>
      <span class="hidden-desktop">
        {{ formattedDateMobile.day }},
        <br />
        {{ formattedDateMobile.remainder }}
      </span>
    </a>
  </div>

  <div class="frame">
    <big-tweet-counts :count="allTweets" :time="calculations.time" />

    <div class="divider" />

    <timeline :tweets="tweets" />

    <div class="mobile-row">
      <small-tweet-count
        v-for="countType in ['tweet', 'retweet', 'retweetWithComment']"
        :key="countType"
        :type="countType"
        :count="calculations[countType]"
        class="column column-small-gutter"
      />
    </div>
  </div>

  <div class="box-bottom button-container">
    <share-buttons :date="date" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'

import { formatDate, formatDateMobile } from '../utils'
import { fetchSingleDate } from '../api'
import BigTweetCounts from './BigTweetCounts.vue'
import ShareButtons from './ShareButtons.vue'
import SmallTweetCount from './SmallTweetCount.vue'
import Timeline from './Timeline.vue'

export default defineComponent({
  components: {
    BigTweetCounts,
    ShareButtons,
    SmallTweetCount,
    Timeline,
  },
  props: {
    date: { type: String, required: true },
  },
  data() {
    return {
      calculations: {
        tweet: 0,
        retweet: 0,
        retweetWithComment: 0,
        time: 0,
      },
      tweets: [],
    }
  },
  computed: {
    allTweets() {
      const { tweet, retweet, retweetWithComment } = this.calculations
      return tweet + retweet + retweetWithComment
    },
    formattedDateDesktop() {
      return formatDate(this.date)
    },
    formattedDateMobile() {
      const [day, remainder] = formatDateMobile(this.date).split(', ')
      return { day, remainder }
    },
  },
  watch: {
    date(newVal) {
      if (newVal) this.fetch(newVal)
    },
  },
  created() {
    this.fetch(this.date)
  },
  methods: {
    async fetch(date) {
      try {
        const response = await fetchSingleDate(date)
        this.calculations = response.calculations
        this.tweets = response.tweets
      } catch (error) {
        console.error(error)
      }
    },
  },
})
</script>

<style scoped>
.box-top {
  margin: 3.75rem 1.75rem 0;
  border: 1px solid white;
  border-bottom: none;
  padding: 1.8125rem;
  font-size: 2.5rem;
  line-height: 1em;
  font-weight: bold;
  text-transform: uppercase;
}

.box-bottom {
  margin: 0 1.75rem 2.75rem;
  padding: 1.625rem;
  border: 1px solid white;
  border-top: none;
  justify-content: center;
}

.frame {
  background: white;
  color: black;
  padding: 2rem 1.75rem;
  text-align: left;
}

.divider {
  background: black;
  height: 1px;
  margin: 2.25rem 0 1.875rem;
}
</style>
