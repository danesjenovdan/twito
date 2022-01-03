<template>
  <div class="container">
    <div class="mx-3">
      <!--      TODO: fix the href so that the page doesn't reload on navigation -->
      <router-link to="/analize/skupne" class="button">{{
        $t('analysis.summarised')
      }}</router-link>
      <router-link to="/analize/dnevne" class="button">{{
        $t('analysis.daily')
      }}</router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import { formatDate } from '../utils'

export default defineComponent({
  props: {
    // date: { type: String, required: true },
  },
})
</script>

<style scoped>
.mx-3 {
  margin: 3rem auto 0 auto;
  display: flex;
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
  cursor: pointer;
}
.button:not(:last-child) {
  margin-bottom: 1rem;
}
.button:hover {
  background: white;
  color: black;
}

.button.router-link-active {
  background-color: #57d9dc;
  border: none;
  color: black;
}

@media (min-width: 768px) {
  .container {
    display: flex;
    justify-content: center;
    align-content: center;
  }

  .button {
    width: 220px;
    margin: 0 0.666rem !important;
  }
}
</style>
