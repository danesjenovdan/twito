<template>
  <div class="date-selection">
    <div>Datum:</div>
    <input type="date" v-model="date" />
  </div>
  <div class="row">
    <div class="column square square-gray">
      <div class="count">{{ tweetCounts.all }}</div>
      {{ pluralize("tweet", tweetCounts.all) }}
    </div>
    <div class="column square square-gray">
      <div class="count">{{ tweetTime }}</div>
      preživel na twitterju
    </div>
  </div>
  <div class="row">
    <div class="column square square-green">
      <div class="count">{{ tweetCounts.original }}</div>
      {{ pluralize("original", tweetCounts.original) }}
      {{ pluralize("tweet", tweetCounts.original) }}
    </div>
    <div class="column square square-orange">
      <div class="count">{{ tweetCounts.retweets }}</div>
      re{{ pluralize("tweet", tweetCounts.retweets) }}
    </div>
    <div class="column square square-yellow">
      <div class="count">{{ tweetCounts.retweetsWithComment }}</div>
      re{{ pluralize("tweet", tweetCounts.retweets) }} s komentarjem
    </div>
  </div>
</template>

<script>
import { getTweetTime, getTweetCounts } from "../timeAnalysis";
import { fetchTweetData } from "../api";

export default {
  data() {
    return {
      tweets: [],
      date: '2020-10-30',
    };
  },
  computed: {
    tweetCounts() {
      return getTweetCounts(this.tweets);
    },
    tweetTime() {
      const tweetTimeInMiliseconds = getTweetTime(this.tweets);
      const tweetTimeInMinutes = Math.round(tweetTimeInMiliseconds / 60000)

      const hours = Math.floor(tweetTimeInMinutes / 60)
      const minutes = String(tweetTimeInMinutes % 60).padStart(2, '0')

      return `${hours}:${minutes}`;
    }
  },
  methods: {
    pluralize(word, count) {
      const WORD_FORMS = {
        original: {
          singular: 'izviren',
          dual: 'izvirna',
          smallPlural: 'izvirni',
          bigPlural: 'izvirnih',
        },
        tweet: {
          singular: 'tweet',
          dual: 'tweeta',
          smallPlural: 'tweeti',
          bigPlural: 'tweetov',
        },
      };

      const getWordForm = (count) => {
        count = count % 100;
        if (count <= 1) {
          return 'singular'
        } else if (count === 2) {
          return 'dual'
        } else if (count < 5) {
          return 'smallPlural'
        }
        return 'bigPlural'
      }

      return WORD_FORMS[word][getWordForm(count)];
    },
    async fetchDataForDate(date) {
      try {
        this.tweets = await fetchTweetData(date);
      } catch (error) {
        console.error(error);
      }
    }
  },
  async created() {
    this.fetchDataForDate(this.date)
  },
  watch: {
    date(newVal) {
      if (newVal) this.fetchDataForDate(newVal)
    }
  }
};
</script>

<style scoped>
@media (min-width: 768px) {
  .row {
    display: flex;
  }
  .column {
    margin: 0 0.5rem;
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
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}
.date-selection input {
  margin-left: 1rem;
  height: 2rem;
}

.square {
  margin-bottom: 1rem;
  text-align: center;
  padding: 1rem;
  border-radius: 0.5rem;
}
.square-gray {
  background: #d8d8d8;
}
.square-green {
  background: #4fe3c1;
}
.square-orange {
  background: #f5a623;
}
.square-yellow {
  background: #f8e71d;
}

.count {
  font-size: 2rem;
  font-weight: bold;
}
</style>
