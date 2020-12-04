<template>
  <modal title="Kako računamo čas?">
    <p>
      S sledilnikom na podlagi aktivnosti Twitter profila
      <a href="https://twitter.com/jjansasds" target="_blank">@jjansasds</a>
      računamo oceno preživetega časa na Twitterju. Dolžino intervala aktivnosti
      začnemo beležiti, ko profil objavi tvit ali ritvit, in jo merimo do
      trenutka, ko po tvitu ali ritvitu več kot 5 minut ni nove objave. Takrat
      sklepamo, da je Twitter aktivnost zaključena. Dokler Maršal objavi vsaj en
      tvit na 5 minut, potem domnevamo, da je njegova pozornost osredotočena
      zgolj na Twitter.
    </p>

    <p>
      Trajanje posameznih intervalov v dnevu nato seštejemo, da dobimo skupno
      oceno dnevno preživetega časa na Twitterju.
    </p>

    <p>
      V intervalih ne upoštevamo premierjevih drugih aktivnosti, kot so
      všečkanje tvitov, saj jih je težje beležiti. Če bi nam rad/-a pomagal/-a
      rešiti to težavo,
      <a href="mailto:vsi@danesjenovdan.si" target="_blank">nam piši</a>.
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
