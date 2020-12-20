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

    <timeline :tweets="tweets" :start-of-day="startOfDay" />

    <div class="mobile-row">
      <small-tweet-count
        v-for="type in Object.values(TweetType)"
        :key="type"
        :type="type"
        :count="calculations[type]"
        class="column column-small-gutter"
      />
    </div>

    <template v-if="!inProduction">
      <div class="divider" />

      <hashtags :hashtags="hashtags" />
    </template>
  </div>

  <div class="box-bottom button-container">
    <share-buttons :date="date" />
  </div>
</template>

<script>
import { defineComponent } from 'vue'

import { TweetType } from '../types'
import { formatDate, formatDateMobile } from '../utils'
import { fetchSingleDate } from '../api'
import BigTweetCounts from './BigTweetCounts.vue'
import Hashtags from './Hashtags.vue'
import ShareButtons from './ShareButtons.vue'
import SmallTweetCount from './SmallTweetCount.vue'
import Timeline from './Timeline.vue'

export default defineComponent({
  components: {
    BigTweetCounts,
    Hashtags,
    ShareButtons,
    SmallTweetCount,
    Timeline,
  },
  inject: ['inProduction'],
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
      hashtags: [],
      tweets: [],
      startOfDay: '',
      TweetType,
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
        this.hashtags = response.hashtags
        this.startOfDay = response.startOfDay
      } catch (error) {
        console.error(error)
      }
    },
  },
})
</script>
