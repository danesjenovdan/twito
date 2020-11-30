<template>
  <modal title="O projektu">
    <p>
      Premier Janez Janša rad tvita. Projekt Maršal Twito – Sledilnik beleži in
      analizira njegovo aktivnost na Twitterju.
    </p>
    <p>
      Projekt želi pokazati na premierjevo zasvojenost z družabnimi omrežji.
      Obenem želi opozoriti tudi na potrebo po večji transparentnosti in
      nadzorom nad aktivnostmi najpomembnejšega človeka v državi, zlasti v času
      epidemije.
    </p>

    <div class="subtitle">Pridruži se</div>
    <p>
      Sledilnik nameravamo razvijati tudi v prihodnosti in redno dodajati nove
      analize. Če imaš znanja in veščine z analiziranjem in vizualizacijo
      podatkov, pa tudi s področja front-end programiranja, nam piši na
      <a href="mailto:vsi@danesjenovdan.si">vsi@danesjenovdan.si</a>.
    </p>

    <div class="subtitle">Avtorji</div>
    <p>
      Za spletno mesto skrbi ekipa Danes je nov dan. Če želiš podpreti naše
      delo, <a href="https://danesjenovdan.si/doniraj">doniraj</a>.
    </p>
    <p>
      Naslovno ilustracijo je ustvaril
      <a href="https://www.stokto.com/">Stokto</a>.
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
