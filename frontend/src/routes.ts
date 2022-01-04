import { RouteRecordRaw } from 'vue-router'
import Main from './Main.vue'
import DayView from './components/DayView.vue'
import Analysis from './components/Analysis.vue'
import AnalysisDaily from './components/AnalysisDaily.vue'
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
    path: '/analize/',
    alias: '/',
    component: Main,
    children: [
      {
        path: '',
        name: 'analize',
        redirect: { name: 'analize-skupne' }
      },
      {
        path: 'skupne',
        name: 'analize-skupne',
        component: Analysis,
      },
      {
        path: 'dnevne',
        component: DayView
      },
      {
        path: ':date?',
        component: AnalysisDaily,
        props: (route) => ({
          date: route.params.date || undefined,
        }),
      },
    ]
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
