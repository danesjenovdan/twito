<template>
  <div class="row">
    <div class="column big-count tweet-count">
      <div class="big-count-label">{{ titleCount }}</div>
      <div class="big-count-stats">
        <div class="big-count-number">{{ count }}</div>
        <div class="tweet-trend" v-if="trendTweetsNo">
          <span>
            <span v-if="trendTweetsNo > 0">+</span>
            <span v-if="trendTweetsNo < 0">-</span>
            {{ Math.abs(trendTweetsNo) }}
            <!-- ({{ trendTweetsPercentage }} %) -->
          </span>
          <img
            v-if="trendTweetsNo < 0"
            src="/icons/trend-negative.png"
            alt="{{ $t('daily.negativeTrendIconAlt') }}"
          />
          <img
            v-if="trendTweetsNo > 0"
            src="/icons/trend-positive.png"
            alt="{{ $t('daily.positiveTrendIconAlt') }}"
          />
        </div>
      </div>
    </div>
    <div class="column big-count tweet-time">
      <div class="big-count-label">
        <div class="help-icon" @click="toggleModal(true)">?</div>
        {{ titleTime }}
      </div>
      <div class="big-count-stats">
        <div class="big-count-number">
          {{ formattedTime.hours }}<span class="time-unit">h</span>
          {{ formattedTime.minutes }}<span class="time-unit">min</span>
        </div>
        <div class="tweet-trend" v-if="trendTime">
          <span>
            <span v-if="trendTime > 0">+</span>
            <span v-if="trendTime < 0">-</span>
            {{ formattedTrendTime.hours }}h {{ formattedTrendTime.minutes }}min
            <!-- ({{ trendTimePercentage }} %) -->
          </span>
          <img
            v-if="trendTime < 0"
            src="/icons/trend-negative.png"
            alt="icon with an arrow showing trend going down"
          />
          <img
            v-if="trendTime > 0"
            src="/icons/trend-positive.png"
            alt="icon with an arrow showing trend going up"
          />
        </div>
      </div>
    </div>
  </div>
  <teleport to="body">
    <modal-methodology v-if="modalOpen" @close="toggleModal(false)" />
  </teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import ModalMethodology from './ModalMethodology.vue'
import { formatSeconds } from '../utils'

export default defineComponent({
  components: {
    ModalMethodology,
  },
  props: {
    titleCount: {type: String, required: true},
    titleTime: {type: String, required: true},
    count: { type: Number, required: true },
    time: { type: Number, required: true },
    trendTweetsNo: { type: Number, required: true },
    trendTweetsPercentage: { type: Number, required: true },
    trendTime: { type: Number, required: true },
    trendTimePercentage: { type: Number, required: true },
  },
  data() {
    return { modalOpen: false }
  },
  computed: {
    formattedTime() {
      return formatSeconds(this.time)
    },
    formattedTrendTime() {
      return formatSeconds(Math.abs(this.trendTime))
    },
  },
  methods: {
    toggleModal(newState) {
      this.modalOpen = newState
    },
  },
})
</script>

<style scoped>
.big-count {
  padding: 1.25rem;
  margin-bottom: 1rem;
  color: #000;
  text-align: left;
}

.big-count-label {
  font-size: 1.125rem;
  line-height: 1em;
  padding-bottom: 0.8125rem;
  border-bottom: 1px solid black;
  margin-bottom: 1.1875rem;
  font-weight: bold;
}

.big-count-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.big-count-number {
  font-size: 5rem;
  line-height: 0.75;
  font-weight: bold;
}

.tweet-trend {
  background-color: #ffffff;
  border-radius: 1.25em;
  padding: 0.75em;
  display: flex;
  align-items: center;
  max-height: 5rem;
}

.tweet-trend > span {
  font-size: 1.125em;
  padding-right: 0.75em;
  font-weight: 500;
}

.tweet-trend img {
  width: 2em;
  height: 2em;
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

.help-icon {
  float: right;
  background: black;
  color: #ffeacc;
  width: 1.25rem;
  height: 1.25rem;
  line-height: 1.334em;
  font-size: 1rem;
  font-weight: bold;
  text-align: center;
  border-radius: 50%;
  cursor: pointer;
  user-select: none;
}

@media (min-width: 992px) {
  .big-count {
    margin-bottom: 0;
  }
}
</style>
