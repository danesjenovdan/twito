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
    <big-tweet-counts
      :count="allTweets"
      :time="calculations.time"
      :trend-tweets-no="calculations.trendTweetsNo"
      :trend-tweets-percentage="calculations.trendTweetsPercentage"
      :trend-time="calculations.trendTime"
      :trend-time-percentage="calculations.trendTimePercentage"
    />

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

      <hashtags :hashtags="hashtags" :domains="domains" :retweets="retweets" />
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
        trendTweetsNo: 0,
        trendTweetsPercentage: 0,
        trendTime: 0,
        trendTimePercentage: 0,
      },
      hashtags: [],
      domains: [],
      retweets: [],
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
      return formatDate(this.date, this.$i18n.locale)
    },
    formattedDateMobile() {
      const [day, remainder] = formatDateMobile(this.date, this.$i18n.locale).split(', ')
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
        // TO DO: BRISI TA DEL VEN, KO BODO TE PODATKI V CALCULATIONS
        this.calculations.trendTweetsNo = 5
        this.calculations.trendTweetsPercentage = 10
        this.calculations.trendTime = -3876
        this.calculations.trendTimePercentage = -5
        // ---------------------------------------------
        this.tweets = response.tweets
        // TO DO: v hashtags spremenit "hashtag" v "tag"
        this.hashtags = response.hashtags
        // TO DO: SPREMENI
        // this.domains = response.domains
        this.domains = [
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
        ]
        // TO DO: SPREMENI
        // this.retweets = response.retweets
        this.retweets = [
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
          { tag: 'Blabla', number: 10 },
        ]
        this.startOfDay = response.startOfDay
      } catch (error) {
        console.error(error)
      }
    },
  },
})
</script>
