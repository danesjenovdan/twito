<template>
  <div class="wrapper">
    <div class="top-stats">
      <div class="label">
        <img
          src="/icons/hashtag.png"
          alt="{{ $t('daily.topStats.hashtagsIconAlt') }}"
        />
        <span>{{ $t('daily.topStats.hashtags') }}</span>
      </div>
      <div class="divider" />
      <div class="top-stats-list">
        <div
          v-for="hashtag in hashtags"
          :key="hashtag.hashtag"
          class="top-stats-list-element"
        >
          <span
            ><a
              :href="`https://twitter.com/search?q=%23${hashtag.hashtag.substring(
                1
              )}`"
              target="_blank"
              >{{ truncate(hashtag.hashtag, 16) }}</a
            ></span
          >
          <span>{{ hashtag.number }}</span>
        </div>
      </div>
    </div>
    <div class="top-stats">
      <div class="label">
        <img
          src="/icons/website.png"
          alt="{{ $t('daily.topStats.domainsIconAlt') }}"
        />
        <span>{{ $t('daily.topStats.domains') }}</span>
      </div>
      <div class="divider" />
      <div class="top-stats-list">
        <div
          v-for="domain in domains"
          :key="domain.tag"
          class="top-stats-list-element"
        >
          <span
            ><a :href="`https://${domain.domain}`" target="_blank">{{
              truncate(domain.domain, 16)
            }}</a></span
          >
          <span>{{ domain.domain_num }}</span>
        </div>
      </div>
    </div>
    <div class="top-stats">
      <div class="label">
        <img
          src="/icons/retweet.png"
          alt="{{ $t('daily.topStats.retweetsIconAlt') }}"
          style="padding: 2px 0"
        />
        <span>{{ $t('daily.topStats.retweets') }}</span>
      </div>
      <div class="divider" />
      <div class="top-stats-list">
        <div
          v-for="retweet in retweets"
          :key="retweet.tag"
          class="top-stats-list-element"
        >
          <span>{{ retweet.tag }}</span>
          <span>{{ retweet.number }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { TweetTop } from '../types'

export default defineComponent({
  props: {
    hashtags: { type: Array as PropType<TweetTop[]>, required: true },
    domains: { type: Array as PropType<TweetTop[]>, required: true },
    retweets: { type: Array as PropType<TweetTop[]>, required: true },
  },
  methods: {
    truncate(str, n) {
      return str.length > n ? str.substr(0, n - 1) + '...' : str
    },
  },
})
</script>

<style scoped>
.wrapper {
  margin: 1.5rem 0;
}
@media (min-width: 768px) {
  .wrapper {
    display: flex;
  }
}
.divider {
  margin: 0;
}
.top-stats {
  border: 5px solid #ddf7f8;
  padding: 1rem;
  margin-bottom: 1em;
  width: 100%;
  display: inline-block;
}
@media (min-width: 768px) {
  .top-stats {
    width: 30%;
    margin-right: 5%;
    margin-bottom: 0;
  }
}
.top-stats:last-child {
  margin-right: 0;
}
.label {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}
.label span {
  font-size: 1.25rem;
  font-weight: bold;
  line-height: 1em;
  margin-left: 0.5rem;
}
.label img {
  height: 25px;
}
.top-stats-list {
  margin: 1rem 1rem 0;
}
.top-stats-list-element {
  line-height: 1.75rem;
}
.top-stats-list-element span:first-child {
  text-decoration: underline;
}
.top-stats-list-element span:last-child {
  font-size: 1.25rem;
  font-weight: 700;
  float: right;
}
</style>
