import _ from 'lodash'
import templateStrings from './templateStrings.json'

export default {
  optimizeDeps: {
    include: ['lodash-es/throttle', 'lodash-es/camelCase'],
  },
  indexHtmlTransforms: [({ code }) => _.template(code)(templateStrings)],
}
