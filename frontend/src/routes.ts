import { RouteRecordRaw } from 'vue-router'
import MenuWrapperView from './components/MenuWrapperView.vue'
import PlainWrapperView from './components/PlainWrapperView.vue'
import DayView from './components/DayView.vue'
import AnalysisView from './components/AnalysisView.vue'
import AboutView from './components/AboutView.vue'
import HowView from './components/HowView.vue'

export default <RouteRecordRaw[]>[
  {
    path: '/',
    component: MenuWrapperView,
    children: [
      {
        path: '/povzetki',
        component: AnalysisView,
      },
      {
        path: '/dnevne-analize',
        alias: '/',
        component: DayView,
      },
      {
        path: '/o-projektu',
        component: AboutView,
      },
      {
        path: '/kako-racunamo',
        component: HowView,
      },
      {
        path: '/:date?',
        component: DayView,
        props: (route) => ({
          date: route.params.date || undefined,
        }),
      },
    ],
  },
  {
    path: '/plain/:date',
    component: PlainWrapperView,
    props: (route) => ({
      date: route.params.date || undefined,
    }),
  },
]
