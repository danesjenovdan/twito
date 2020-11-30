import _ from 'lodash'
import templateStrings from './templateStrings.json'

export default {
  optimizeDeps: {
    include: [
      'lodash-es/camelCase',
      'lodash-es/capitalize',
      'lodash-es/mapKeys',
      'lodash-es/throttle',
    ],
  },
  indexHtmlTransforms: [({ code }) => _.template(code)(templateStrings)],
}
