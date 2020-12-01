<template>
  <modal title="O projektu">
    <p>
      Premier Janez Janša veliko tvita. Projekt <i>Maršal Twito – Sledilnik</i> beleži
      in analizira njegovo aktivnost na Twitterju.
    </p>
    <p>
      Tvitanje je eden Janševih osrednjih političnih instrumentov. Kot predsednik vlade
      državljanom in medijem na Twitterju sporoča pomembne odločitve, ukrepe in poteze.
      Obenem pa ga uporablja za utrjevanje strankarske baze, mobilizacijo skrajne desnice
      in dajanje potuhe sovražnemu govoru.
    </p>
    <p>
      Videti je, da tvite večinoma piše sam, glede na njihovo pogostost (še posebno ritvitov) pa
      je mogoče slutiti, da na omrežju preživlja veliko časa. Dokler je v funkciji predsednika
      vlade in to še posebej v času epidemije, je njegova zasvojenost z družbenimi omrežji
      zaskrbljujoča in pomembna za širšo družbo.
    </p>
    <p>
      Projekt Maršal Twito – Sledilnik želi opozoriti na to stanje in z analizo podatkov
      pridobiti vpogled v propagandistično aktivnost najbolj vplivnega Twitter profila v državi.
    </p>

    <div class="subtitle">Pridruži se</div>
    <p>
      Sledilnik nameravamo razvijati tudi v prihodnosti in redno dodajati nove analize. Če imaš
      znanja in veščine z analiziranjem in vizualizacijo podatkov, pa tudi s področja front-end
      programiranja, nam piši na <a href="mailto:vsi@danesjenovdan.si">vsi@danesjenovdan.si</a>.
    </p>

    <div class="subtitle">Avtorji</div>
    <p>
      Za spletno mesto skrbi ekipa <a href="https://danesjenovdan.si/">Danes je nov dan</a>. Če
      želiš podpreti naše delo, lahko <a href="https://danesjenovdan.si/doniraj">doniraš</a>.
    </p>
    <p>
      Naslovno ilustracijo je ustvaril <a href="https://www.stokto.com/">Stokto</a>.
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
