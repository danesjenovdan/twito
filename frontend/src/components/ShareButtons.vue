<template>
  <div class="container">
    <a :href="shareUrls.link" class="button">{{ $t('daily.share.shareLink') }}</a>
    <a :href="shareUrls.facebook" class="button">{{ $t('daily.share.shareFB') }}</a>
    <a :href="shareUrls.twitter" class="button">{{ $t('daily.share.shareTW') }}</a>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import { formatDate } from '../utils'

export default defineComponent({
  props: {
    date: { type: String, required: true },
  },
  computed: {
    shareUrls() {
      const text = encodeURIComponent(
        `${formatDate(this.date)} // Maršal Twito - Sledilnik`
      )
      const url = encodeURIComponent(`https://twito.si/${this.date}`)
      return {
        facebook: `https://www.facebook.com/dialog/feed?app_id=381430693089489&redirect_uri=${url}&link=${url}&ref=responsive&name=${text}`,
        twitter: `https://twitter.com/intent/tweet?text=${text}%20${url}`,
        link: decodeURIComponent(url),
      }
    },
  },
})
</script>

<style scoped>
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
  .container {
    display: flex;
    justify-content: center;
  }

  .button {
    width: 11.625rem;
    margin: 0 0.666rem !important;
  }
}
</style>
