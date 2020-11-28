<template>
  <div class="overlay" @click="close">
    <div class="container" @click.stop>
      <div class="close-button" @click="close">×</div>

      <div class="title">O projektu</div>

      <p>
        Premier Janez Janša rad tvita. Projekt Maršal Twito – Sledilnik beleži
        in analizira njegovo aktivnost na Twitterju.
      </p>
      <p>
        Projekt želi pokazati na premierjevo zasvojenost z družabnimi omrežji.
        Obenem želi opozoriti tudi na potrebo po večji transparentnosti in
        nadzorom nad aktivnostmi najpomembnejšega človeka v državi, zlasti v
        času epidemije.
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
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  methods: {
    close() {
      this.$emit('close')
    },
    print() {
      console.log('foo')
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
  padding: 4.125rem;
  width: 100%;
  background: white;
  max-width: 52.5rem;
  font-size: 1.25rem;
  position: relative;
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
}

.subtitle {
  text-transform: uppercase;
  font-size: 2rem;
  margin-top: 3rem;
  margin-bottom: 0.25rem;
}

p {
  line-height: 1.75em;
  margin: 0 0 0.75em;
}

a {
  color: inherit;
}
</style>
