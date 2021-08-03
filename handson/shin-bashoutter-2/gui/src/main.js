import Vue from 'vue'
import Vuex from 'vuex'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import "@aws-amplify/ui-vue";
import Amplify from "aws-amplify";
import awsconfig from "./aws-exports";
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'

Amplify.configure(awsconfig);

Vue.config.productionTip = false
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    url: "https://api.bashoutter.com",
  },
  mutations: {
    set_url (state, url) {
      state.url = url;
    }
  }
})

new Vue({
  vuetify,
  store: store,
  render: h => h(App)
}).$mount('#app')
