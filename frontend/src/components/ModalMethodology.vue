<template>
  <modal title="Kako računamo čas?">
    <p>
      S sledilnikom na podlagi aktivnosti profila @jjansasds računamo oceno
      preživetega časa na Twitterju. Interval časovne aktivnosti začnemo
      beležiti ob prvem tvitu ali ritvitu. Če se v 5 minutah po zadnjem tvitu
      ali retvitu ne zgodi nič, interval zaključimo, saj sklepamo, da se je
      trenutna aktivnost končala.
    </p>

    <p>
      Trajanje posameznih intervalov nato seštejemo, da dobimo oceno dnevno
      preživetega časa na Twitterju.
    </p>

    <p>
      V intervalih ne upoštevamo premierjevih drugih aktivnosti, kot so
      všečkanje tvitov, saj jih je težje beležiti. Če bi nam rad/-a pomagal/-a
      rešiti to težavo, nam <a href="mailto:vsi@danesjenovdan.si">piši</a>.
    </p>
  </modal>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

import Modal from './Modal.vue'

export default defineComponent({
  components: { Modal },
})
</script>
