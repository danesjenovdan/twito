<template>
  <div class="date-selection">
    <div>Datum:</div>
    <input type="date" v-model="date" />
  </div>

  <div class="box-top">
    Torek, 10. november 2020
  </div>

  <div class="frame">
    <div class="row">
      <div class="column big-count tweet-count">
        <div class="big-count-label">število tweetov</div>
        <div class="big-count-number">{{ tweetCounts.all }}</div>
      </div>
      <div class="column big-count tweet-time">
        <div class="big-count-label">ocena časa, preživetega na Twitterju</div>
        <div class="big-count-number">
          {{ tweetTime.hours }}<span class="time-unit">h</span>
          {{ tweetTime.minutes }}<span class="time-unit">min</span>
        </div>
      </div>
    </div>
  </div>

  <div class="box-middle" />

  <div class="frame">
    <timeline :tweets="tweets" />
  </div>

  <div class="frame">
    <div class="row">
      <div class="column small-count original">
        <div class="small-count-label">izvirni tviti</div>
        <div class="small-count-number">{{ tweetCounts.original }}</div>
      </div>
      <div class="column small-count retweets">
        <div class="small-count-label">RT-ji</div>
        <div class="small-count-number">{{ tweetCounts.retweets }}</div>
      </div>
      <div class="column small-count retweets-with-comment">
        <div class="small-count-label">RT-ji s komentarjem</div>
        <div class="small-count-number">{{ tweetCounts.retweetsWithComment }}</div>
      </div>
    </div>
  </div>

  <div class="box-bottom">
    <div class="button">Prenesi</div>
    <div class="button">Deli na FB</div>
    <div class="button">Deli na TW</div>
  </div>
</template>

<script>
import { getTweetTime, getTweetCounts } from "../utils";
import { fetchTweetData } from "../api";
import Timeline from "./Timeline.vue";

export default {
  components: {
    Timeline,
  },
  data() {
    return {
      tweets: [],
      date: "2020-10-30",
    };
  },
  computed: {
    tweetCounts() {
      return getTweetCounts(this.tweets);
    },
    tweetTime() {
      const tweetTimeInMiliseconds = getTweetTime(this.tweets);
      const tweetTimeInMinutes = Math.round(tweetTimeInMiliseconds / 60000);

      const hours = Math.floor(tweetTimeInMinutes / 60);
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, "0");

      return { hours, minutes};
    },
  },
  methods: {
    async fetchDataForDate(date) {
      try {
        this.tweets = await fetchTweetData(date);
      } catch (error) {
        console.error(error);
      }
    },
  },
  async created() {
    this.fetchDataForDate(this.date);
  },
  watch: {
    date(newVal) {
      if (newVal) this.fetchDataForDate(newVal);
    },
  },
};
</script>

<style scoped>
.box-top {
  margin: 4rem 2.5rem 0;
  border: 1px solid white;
  border-bottom: none;
  padding: 2.5rem;
  font-size: 50px;
  line-height: 1em;
  font-weight: bold;
  text-transform: uppercase;
}

.box-middle {
  margin: 0 2.5rem;
  border-left: 1px solid white;
  border-right: 1px solid white;
  height: 3.125rem;
}

.box-bottom {
  margin: 0 2.5rem 4rem;
  padding: 2.5rem;
  border: 1px solid white;
  border-top: none;
  display: flex;
  justify-content: center;
}

.frame {
  background: white;
  color: black;
  padding: 2.5rem;
  text-align: left;
}


.big-count {
  padding: 1.5rem;
}

.big-count-label {
  font-size: 1.25rem;
  line-height: 1em;
  padding-bottom: 1rem;
  border-bottom: 1px solid black;
  margin-bottom: 1.25rem;
  font-weight: bold;
}

.big-count-number {
  font-size: 6.25rem;
  line-height: 1em;
  font-weight: bold;
  height: 6rem;
}

.time-unit { font-size: 0.5em }

.tweet-count {
  background: #ddf7f8;
}

.tweet-time {
  background: #ffeacc;
  flex: 2;
}

.small-count {
  padding: 1rem;
}

.small-count-label {
  margin-bottom: 0.75rem;
}

.small-count-number {
  font-size: 4.375rem;
  line-height: 1em;
  font-weight: bold;
  height: 4.375rem;
}

.original {
  background-color: #ffedeb;
  border: 5px solid #ff4e3a;
}

.retweets {
  border: 5px solid #44a58a;
background-color: #ecf6f3;
}

.retweets-with-comment {
  border: 5px solid #ffc208;
background-color: #fff9e6;
}

.button {
  border: 1px solid white;
  border-radius: 1.75rem;
  height: 3.5rem;
  line-height: 3.25rem;
  font-size: 1.875rem;
  font-weight: bold;
  text-transform: uppercase;
  margin: 0 1rem;
  width: 15.125rem;
  cursor: pointer;
}
.button:hover {
  background: white;
  color: black;
}

@media (min-width: 768px) {
  .row {
    display: flex;
  }
  .column {
    margin: 0 1.25rem;
    flex: 1;
  }
  .column:first-child {
    margin-left: 0;
  }
  .column:last-child {
    margin-right: 0;
  }
}

.date-selection {
  position: absolute;
  top: 0;
  left: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}
.date-selection input {
  margin-left: 1rem;
  height: 2rem;
}
</style>
