import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import routes from './routes'
import './index.css'
import si from './locales/si.json'
import en from './locales/en.json'

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const i18n = createI18n({
  locale: 'si',
  messages: {
    si: si,
    en: en,
  },
})

createApp(App).use(router).use(i18n).mount('#app')
