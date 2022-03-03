<template>
  <div class="wrapper">
    <div class="sidebar" :class="{'hidden': !showNavigationMenu }">
      <div class="navigation">
        <router-link to="/dnevne-analize" class="navigation-link uppercase">{{ $t('analysis.daily') }}</router-link>
         <router-link to="/povzetki" class="navigation-link uppercase">{{ $t('analysis.title') }}</router-link>
        <router-link to="/o-projektu" class="navigation-link uppercase">{{ $t('about.title') }}</router-link>
        <router-link to="/kako-racunamo" class="navigation-link uppercase">{{ $t('methodology.title') }}</router-link>
        <a href="https://twitter.com/twitosledilnik" target="_blank" class="navigation-link">@twitosledilnik</a>
        <a href="https://danesjenovdan.si/" target="_blank" class="navigation-link">{{ $t('djnd') }}</a>
        <div class="mobile-close-navigation" @click="showNavigationMenu = false">×</div>
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
      <div>
        <div class="mobile-navigation-button" @click="togglenNavigationMenu">
          <img src="/public/icons/open-menu.svg" />
        </div>
        <div class="container">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({
  data() {
    return {
      showNavigationMenu: false
    }
  },
  watch: {
    $route() {
      this.showNavigationMenu = false;
    }
  },
  methods: {
    togglenNavigationMenu() {
      this.showNavigationMenu = !this.showNavigationMenu;
    }
  }
})
</script>


<style scoped>

.wrapper {
  overflow-x: hidden;
}

.navigation {
  padding: 30px;
}

.mobile-navigation-button {
  display: none;
  text-align: right;
  font-weight: 300;
  font-size: 20px;
  text-decoration: none;
  border-bottom: 1px solid white;
  margin: 20px 0;
  padding-bottom: 10px;
}

.mobile-navigation-button img {
  height: 20px;
}

.mobile-close-navigation {
  display: none;
  position: absolute;
  right: 20px;
  top: 20px;
  font-size: 32px;
  line-height: 28px;
  font-weight: 300;
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

.navigation-link:nth-child(4) {
  margin-bottom: 60px;
}

.sidebar {
  background-color: #151515;
  width: 300px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: fixed;
  transition: all 0.5s ease-in-out;
  z-index: 1;
}

.container {
  max-width: 978px;
  margin: 0 auto;
  margin-bottom: 60px;
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
  margin-left: 300px;
  padding: 0 50px;
}

@media (max-width: 767.98px) {
  
  .sidebar.hidden {
    left: -100%;
  }
  .sidebar {
    left: 0;
  }

  .mobile-navigation-button {
    display: block;
  }

  .mobile-close-navigation {
    display: block;
  }

  .content {
    margin-left: 0;
    width: 100%;
    padding: 0 20px;
  }
  
}

@media (max-width: 575.98px) {
  .sidebar {
    width: 100%;
  }
  
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