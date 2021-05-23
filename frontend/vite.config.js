import vue from '@vitejs/plugin-vue'

export default {
  plugins: [vue()],
  optimizeDeps: {
    include: [
      'lodash-es/camelCase',
      'lodash-es/capitalize',
      'lodash-es/forEach',
      'lodash-es/mapKeys',
      'lodash-es/mapValues',
    ],
  },
}
