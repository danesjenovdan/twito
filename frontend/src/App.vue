<template>
  <div class="wrapper">
    <div class="sidebar">
      <div class="navigation">
        <router-link to="/analize" class="navigation-link uppercase">{{ $t('analysis.title') }}</router-link>
        <router-link to="/o-projektu" class="navigation-link uppercase">{{ $t('about.title') }}</router-link>
        <router-link to="/kako-racunamo" class="navigation-link uppercase">{{ $t('methodology.title') }}</router-link>
        <a href="https://twitter.com/twitosledilnik" target="_blank" class="navigation-link">@twitosledilnik</a>
        <a href="https://danesjenovdan.si/" target="_blank" class="navigation-link">{{ $t('djnd') }}</a>
        <div class="locale-changer">
        <span
          v-for="locale in $i18n.availableLocales"
          :key="`locale-${locale}`"
          @click="$i18n.locale = locale"
          :class="{ active: $i18n.locale === locale }"
        >
          {{ locale }}
        </span>
      </div>
      </div>
      <div class="twito">
        <div class="twito-title-img">
          <img src="/public/marsal-twito.png" />
        </div>
        <div class="twito-img">
          <img src="/public/twito-transparent.png" />
        </div>
      </div>
    </div>
    <div class="content">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>

.wrapper {
  display: flex;
}

.navigation {
  padding: 30px;
}

.navigation-link {
  font-weight: 300;
  font-size: 20px;
  text-decoration: none;
  display: block;
  margin-bottom: 20px;
  text-align: left;
}

.navigation-link:hover {
  text-decoration: underline;
}

.navigation-link.router-link-active {
  font-weight: 700;
  text-decoration: underline;
}

.navigation-link:nth-child(3) {
  margin-bottom: 60px;
}

.sidebar {
  background-color: #151515;
  width: 300px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: fixed;
}

.twito-title-img {
  display: flex;
  justify-content: center;
}

.twito-title-img img {
  display: block;
  margin-bottom: 30px;
}

.twito-img img {
  display: block;
  width: 100%;
}

.content {
  flex-grow: 1;
  margin-left: 300px;
  padding: 0 50px;
}

.locale-changer {
  text-transform: uppercase;
  text-align: left;
}

.locale-changer span {
  cursor: pointer;
  font-size: 20px;
  font-weight: 300;
}

.locale-changer span:last-child {
  padding-left: 1rem;
}

.locale-changer span.active {
  text-decoration: underline;
}

.locale-changer span:not(:last-child):after {
  content: '/';
  position: absolute;
  padding-left: 0.25rem;
}

.uppercase {
  text-transform: uppercase;
}

</style>