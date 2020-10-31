<template>
  <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld msg="Hello Vue 3.0 + Vite" />
  {{ tweets }}
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";
import { generateIntervals, calculateTweetTime } from "./timeAnalysis";

const API_URL = import.meta.env.VITE_API_URL;

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  data() {
    return {
      tweets: [],
    };
  },
  created() {
    this.fetchTweetData();
  },
  methods: {
    async fetchTweetData() {
      try {
        const response = await fetch(`${API_URL}2020-10-30`);
        if (response.status !== 200) {
          console.log(
            "Looks like there was a problem. Status Code: " + response.status
          );
          return;
        }
        const tweets = await response.json();
        this.tweets = tweets;
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
