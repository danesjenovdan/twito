<template>
  <modal :title="$t('methodology.title')">
    <i18n-t keypath="methodology.desc1" tag="p">
      <a href="https://twitter.com/jjansasds" target="_blank">@jjansasds</a>
    </i18n-t>

    <p>{{ $t('methodology.desc2') }}</p>

    <i18n-t keypath="methodology.desc3" tag="p">
      <a href="mailto:vsi@danesjenovdan.si" target="_blank">{{ $t('methodology.mailLink') }}</a>
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
