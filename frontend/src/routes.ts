import { RouteRecordRaw } from 'vue-router'
import Main from './Main.vue'

export default <RouteRecordRaw[]>[
  {
    path: '/:date?',
    component: Main,
    props: (route) => ({
      date: route.params.date || undefined,
    }),
  },
]
