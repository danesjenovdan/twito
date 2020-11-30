<template>
  <div class="overlay" @click="close">
    <div class="container" @click.stop>
      <div class="close-button" @click="close">×</div>

      <div class="title">{{ title }}</div>

      <slot></slot>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    title: { type: String, required: true },
  },
  methods: {
    close() {
      this.$emit('close')
    },
  },
})
</script>

<style scoped>
.overlay {
  position: fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  padding: 2rem;
}

.container {
  color: black;
  padding: 2rem;
  width: 100%;
  background: white;
  max-width: 52.5rem;
  max-height: calc(100vh - 4rem);
  font-size: 1.25rem;
  position: relative;
  overflow-y: auto;
}

.close-button {
  width: 2.8125rem;
  height: 2.8125rem;
  position: absolute;
  top: 2.1875rem;
  right: 1.5625rem;
  background: black;
  color: white;
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 1.75rem;
  padding-right: 1.75rem;
}

::v-deep(.subtitle) {
  text-transform: uppercase;
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 0.25rem;
}

::v-deep(p) {
  line-height: 1.75em;
  margin: 0 0 0.75em;
}

::v-deep(p:last-child) {
  margin: 0;
}

::v-deep(a) {
  color: inherit;
}

@media (min-width: 768px) {
  .container {
    padding: 4.125rem;
  }
}
</style>
