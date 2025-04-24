import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import './assets/global.css' // 导入全局CSS

// 配置axios
axios.defaults.baseURL = 'http://localhost:5000' // 后端API基础URL
axios.defaults.timeout = 15000 // 15秒超时
axios.defaults.headers.post['Content-Type'] = 'application/json'

// 请求拦截器
axios.interceptors.request.use(
  config => {
    console.log(`请求 ${config.method.toUpperCase()} ${config.url}`)
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
axios.interceptors.response.use(
  response => {
    console.log(`响应 ${response.config.url}:`, response.status)
    return response
  },
  error => {
    if (error.response) {
      console.error(`响应错误 ${error.response.status}:`, error.response.data)
    } else if (error.request) {
      console.error('未收到响应:', error.request)
    } else {
      console.error('请求配置错误:', error.message)
    }
    return Promise.reject(error)
  }
)

Vue.config.productionTip = false

// 将axios添加到Vue原型上，可以通过this.$http访问
Vue.prototype.$http = axios

// 添加全局过渡效果
router.beforeEach((to, from, next) => {
  store.commit('SET_LOADING', true)
  next()
})

router.afterEach(() => {
  setTimeout(() => store.commit('SET_LOADING', false), 500)
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app') 