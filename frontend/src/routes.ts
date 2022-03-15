import { RouteRecordRaw } from 'vue-router'
import DayView from './components/DayView.vue'
import Analysis from './components/Analysis.vue'
import About from './components/About.vue'
import How from './components/How.vue'


export default <RouteRecordRaw[]>[
  {
    path: '/:date?',
    component: DayView,
    props: (route) => ({
      date: route.params.date || undefined,
    }),
  },
  {
    path: '/povzetki',
    component: Analysis,
  },
  {
    path: '/dnevne-analize',
    alias: '/',
    component: DayView
  },
  {
    path: '/o-projektu',
    component: About
  },
  {
    path: '/kako-racunamo',
    component: How
  },
]
