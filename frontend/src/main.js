import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'

// 设置全局axios默认值
axios.defaults.baseURL = 'http://localhost:5000'
Vue.prototype.$http = axios

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app') 