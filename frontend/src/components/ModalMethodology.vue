<template>
  <modal :title="$t('modalMethodology.title')">
    <i18n-t keypath="modalMethodology.desc1" tag="p">
      <a href="https://twitter.com/jjansasds" target="_blank">@jjansasds</a>
    </i18n-t>

    <p>{{ $t('modalMethodology.desc2') }}</p>

    <i18n-t keypath="modalMethodology.desc3" tag="p">
      <a href="mailto:vsi@danesjenovdan.si" target="_blank">{{ $t('modalMethodology.mailLink') }}</a>
    </i18n-t>
  </modal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import Modal from './Modal.vue'

export default defineComponent({
  components: { Modal },
})
</script>
