<template>
  <div class="row">
    <div class="column big-count tweet-count">
      <div class="big-count-label">število tvitov</div>
      <div class="big-count-number">{{ count }}</div>
    </div>
    <div class="column big-count tweet-time">
      <div class="big-count-label">
        <div class="help-icon" @click="toggleModal(true)">?</div>
        ocena preživetega časa na Twitterju
      </div>
      <div class="big-count-number">
        {{ formattedTime.hours }}<span class="time-unit">h</span>
        {{ formattedTime.minutes }}<span class="time-unit">min</span>
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

export default defineComponent({
  components: {
    ModalMethodology,
  },
  props: {
    count: { type: Number, required: true },
    time: { type: Number, required: true },
  },
  data() {
    return { modalOpen: false }
  },
  computed: {
    formattedTime() {
      const tweetTimeInMinutes = Math.round(this.time / 60)

      const hours = Math.floor(tweetTimeInMinutes / 60)
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, '0')

      return { hours, minutes }
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
}

.big-count-label {
  font-size: 1.25rem;
  line-height: 1em;
  padding-bottom: 0.8125rem;
  border-bottom: 1px solid black;
  margin-bottom: 1.1875rem;
  font-weight: bold;
}

.big-count-number {
  font-size: 5rem;
  line-height: 0.725em;
  font-weight: bold;
  height: 0.725em;
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

@media (min-width: 768px) {
  .big-count {
    margin-bottom: 0;
  }
}
</style>
