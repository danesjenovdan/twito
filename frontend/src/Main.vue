<template>
  <div class="container">
    <ViewButtons></ViewButtons>
    <router-view></router-view>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

import ViewButtons from './components/ViewButtons.vue'

export default defineComponent({
  components: {
    ViewButtons,
  },
})
</script>

<style scoped>

.container {
  max-width: 978px;
  margin: 0 auto;
  margin-bottom: 60px;
}

</style>
