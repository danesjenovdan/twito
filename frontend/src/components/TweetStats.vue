<template>
  <div class="box-top">
    {{ formattedDate }}
  </div>

  <div class="frame">
    <big-tweet-counts :count="tweetCounts.all" :time="tweetTime" />

    <div class="divider" />

    <timeline :tweets="tweets" />

    <div class="row">
      <small-tweet-count
        v-for="countType in ['original', 'retweets', 'retweetsWithComment']"
        :key="countType"
        :type="countType"
        :count="tweetCounts[countType]"
        class="column column-small-gutter"
      />
    </div>
  </div>

  <div class="box-bottom button-container">
    <div class="button">Prenesi</div>
    <a :href="shareUrls.facebook" class="button">Deli na FB</a>
    <a :href="shareUrls.twitter" class="button">Deli na TW</a>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import format from 'date-fns/format'
import { sl } from 'date-fns/locale'

import { getTweetTime, getTweetCounts } from '../utils'
import { fetchTweetData } from '../api'
import BigTweetCounts from './BigTweetCounts.vue'
import SmallTweetCount from './SmallTweetCount.vue'
import Timeline from './Timeline.vue'

export default defineComponent({
  components: {
    BigTweetCounts,
    SmallTweetCount,
    Timeline,
  },
  props: {
    date: { type: String, required: true },
  },
  data() {
    return {
      tweets: [],
    }
  },
  computed: {
    tweetCounts() {
      return getTweetCounts(this.tweets)
    },
    tweetTime() {
      return getTweetTime(this.tweets)
    },
    formattedDate() {
      return format(new Date(this.date), 'EEEE, d. MMMM y', { locale: sl })
    },
    shareUrls() {
      const text = encodeURIComponent('Maršal Twito.')
      const url = encodeURIComponent(`https://twito.si/#/${this.date}`)
      return {
        facebook: `https://www.facebook.com/dialog/feed?app_id=301375193309601&redirect_uri=${url}&link=${url}&ref=responsive&name=${text}`,
        twitter: `https://twitter.com/intent/tweet?text=${text}%20${url}`,
      }
    },
  },
  watch: {
    date(newVal) {
      if (newVal) this.fetchDataForDate(newVal)
    },
  },
  async created() {
    this.fetchDataForDate(this.date)
  },
  methods: {
    async fetchDataForDate(date) {
      try {
        this.tweets = await fetchTweetData(date)
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

.button {
  color: inherit;
  display: block;
  text-decoration: none;
  border: 1px solid white;
  border-radius: 1.4rem;
  height: 2.8rem;
  line-height: 2.625rem;
  font-size: 1.25rem;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
}
.button:not(:last-child) {
  margin-bottom: 1rem;
}
.button:hover {
  background: white;
  color: black;
}

@media (min-width: 768px) {
  .button-container {
    display: flex;
    justify-content: center;
  }

  .button {
    width: 11.625rem;
    margin: 0 0.666rem !important;
  }
}
</style>
