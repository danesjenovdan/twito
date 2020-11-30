<template>
  <div class="link-container">
    <div class="link" @click="toggleMethodologyModal(true)">
      Kako računamo čas?
    </div>
    <div class="link" @click="toggleAboutModal(true)">O projektu</div>
    <a class="link" href="https://danesjenovdan.si/">Danes je nov dan</a>
  </div>
  <teleport to="body">
    <modal-methodology
      v-if="methodologyModalOpen"
      @close="toggleMethodologyModal(false)"
    />
    <modal-about v-if="aboutModalOpen" @close="toggleAboutModal(false)" />
  </teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import ModalMethodology from './ModalMethodology.vue'
import ModalAbout from './ModalAbout.vue'

export default defineComponent({
  components: {
    ModalAbout,
    ModalMethodology,
  },
  data() {
    return {
      aboutModalOpen: false,
      methodologyModalOpen: false,
    }
  },
  methods: {
    toggleMethodologyModal(newState) {
      this.methodologyModalOpen = newState
    },
    toggleAboutModal(newState) {
      this.aboutModalOpen = newState
    },
  },
})
</script>

<style scoped>
.link-container {
  background: black;
  bottom: 0;
  padding: 1rem;
  position: fixed;
  right: 0;
}

.link {
  color: #ffeacc;
  display: block;
  font-size: 1rem;
  line-height: 2.25rem;
  text-align: right;
  text-decoration: underline;
}
.link:hover {
  cursor: pointer;
  font-weight: bold;
}
</style>
