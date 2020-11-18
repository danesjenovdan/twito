<template>
  <div class="box-top">
    {{ formattedDate }}
  </div>

  <div class="frame">
    <div class="row">
      <div class="column big-count tweet-count">
        <div class="big-count-label">število tweetov</div>
        <div class="big-count-number">{{ tweetCounts.all }}</div>
      </div>
      <div class="column big-count tweet-time">
        <div class="big-count-label">ocena časa, preživetega na Twitterju</div>
        <div class="big-count-number">
          {{ tweetTime.hours }}<span class="time-unit">h</span>
          {{ tweetTime.minutes }}<span class="time-unit">min</span>
        </div>
      </div>
    </div>
  </div>

  <div class="box-middle" />

  <div class="frame">
    <timeline :tweets="tweets" />
  </div>

  <div class="frame">
    <div class="row">
      <small-tweet-count
        v-for="countType in ['original', 'retweets', 'retweetsWithComment']"
        :key="countType"
        :type="countType"
        :count="tweetCounts[countType]"
        class="column"
      />
    </div>
  </div>

  <div class="box-bottom row">
    <div class="button column">Prenesi</div>
    <a :href="shareUrls.facebook" class="button column">Deli na FB</a>
    <a :href="shareUrls.twitter" class="button column">Deli na TW</a>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import format from 'date-fns/format'
import { sl } from 'date-fns/locale'

import { getTweetTime, getTweetCounts } from '../utils'
import { fetchTweetData } from '../api'
import SmallTweetCount from './SmallTweetCount.vue'
import Timeline from './Timeline.vue'

export default defineComponent({
  components: {
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
      const tweetTimeInMiliseconds = getTweetTime(this.tweets)
      const tweetTimeInMinutes = Math.round(tweetTimeInMiliseconds / 60000)

      const hours = Math.floor(tweetTimeInMinutes / 60)
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, '0')

      return { hours, minutes }
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
  margin: 4rem 2.5rem 0;
  border: 1px solid white;
  border-bottom: none;
  padding: 2.5rem;
  font-size: 3.125rem;
  line-height: 1em;
  font-weight: bold;
  text-transform: uppercase;
}

.box-middle {
  margin: 0 2.5rem;
  border-left: 1px solid white;
  border-right: 1px solid white;
  height: 3.125rem;
}

.box-bottom {
  margin: 0 2.5rem 4rem;
  padding: 2.5rem;
  border: 1px solid white;
  border-top: none;
  justify-content: center;
}

.frame {
  background: white;
  color: black;
  padding: 2.5rem;
  text-align: left;
}

.big-count {
  padding: 1.5rem;
}

.big-count-label {
  font-size: 1.25rem;
  line-height: 1em;
  padding-bottom: 1rem;
  border-bottom: 1px solid black;
  margin-bottom: 1.25rem;
  font-weight: bold;
}

.big-count-number {
  font-size: 6.25rem;
  line-height: 1em;
  font-weight: bold;
  height: 6rem;
}

.time-unit {
  font-size: 0.5em;
}

.tweet-count {
  background: #ddf7f8;
}

.tweet-time {
  background: #ffeacc;
  flex: 2;
}

.button {
  color: inherit;
  display: block;
  text-decoration: none;
  border: 1px solid white;
  border-radius: 1.75rem;
  height: 3.5rem;
  line-height: 3.25rem;
  font-size: 1.875rem;
  font-weight: bold;
  text-transform: uppercase;
  cursor: pointer;
}
.button:hover {
  background: white;
  color: black;
}
</style>
