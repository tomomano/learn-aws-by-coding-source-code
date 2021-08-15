import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    url: "https://api.neuralartcanvas.org",
    jobId: "",
  },
  mutations: {
    set_url (state, url) {
      state.url = url;
    },
    set_job_id (state, value) {
      state.jobId = value;
    }
  }
})

new Vue({
  vuetify,
  store: store,
  render: h => h(App)
}).$mount('#app')
