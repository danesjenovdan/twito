import { RouteRecordRaw } from 'vue-router'
import Main from './Main.vue'
import DayView from './components/DayView.vue'

export default <RouteRecordRaw[]>[
  {
    path: '/:date?',
    component: Main,
    props: (route) => ({
      date: route.params.date || undefined,
    }),
  },
  {
    path: '/d',
    component: DayView,
  },
]
