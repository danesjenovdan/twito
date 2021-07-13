<template>
  <modal :title="$t('modalAbout.title')">
    <i18n-t keypath="modalAbout.desc1" tag="p">
      <i>{{ $t('projectName') }}</i>
    </i18n-t>
    <p>
      {{ $t('modalAbout.desc2') }}
    </p>
    <p>
      {{ $t('modalAbout.desc3') }}
    </p>
    <p>
      {{ $t('modalAbout.desc4') }}
    </p>

    <div class="subtitle">{{ $t('modalAbout.subtitle1') }}</div>
    <i18n-t keypath="modalAbout.desc5" tag="p">
      <a href="mailto:vsi@danesjenovdan.si">vsi@danesjenovdan.si</a>
    </i18n-t>

    <div class="subtitle">{{ $t('modalAbout.subtitle2') }}</div>
    <i18n-t keypath="modalAbout.desc6" tag="p">
      <a href="https://danesjenovdan.si/">{{ $t('djnd') }}</a>
      <a href="https://danesjenovdan.si/doniraj">{{ $t('modalAbout.donate') }}</a>
    </i18n-t>
    <i18n-t keypath="modalAbout.desc7" tag="p">
      <a href="https://www.stokto.com/">Stokto</a>
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
