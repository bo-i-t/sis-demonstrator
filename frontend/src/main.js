import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import VueRecord from '@codekraft-studio/vue-record'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueAxios from 'vue-axios'
import axios from 'axios'
import VueRouter from 'vue-router'
import router from './router'
import { CardPlugin } from 'bootstrap-vue'
import { BCard } from 'bootstrap-vue'
import VueSession from 'vue-session'

Vue.use(VueSession)
Vue.use(VueAxios, axios)
Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(CardPlugin)
Vue.component('b-card', BCard)
Vue.use(VueRecord)

Vue.config.productionTip = false
Vue.use(VueRouter)

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
