import _ from 'lodash'
import vue from '@vitejs/plugin-vue'

// import templateStrings from './templateStrings.json'

export default {
  plugins: [
    vue(),
  ],
  optimizeDeps: {
    include: [
      'lodash-es/camelCase',
      'lodash-es/capitalize',
      'lodash-es/forEach',
      'lodash-es/mapKeys',
      'lodash-es/mapValues',
    ],
  },
  indexHtmlTransforms: [({ code }) => _.template(code)(templateStrings)],
}
