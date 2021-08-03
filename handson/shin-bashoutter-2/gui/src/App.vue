<template>
  <v-app>
    <v-app-bar
      app
      color="blue"
      dark
    >
      <v-btn icon>
        <v-icon>mdi-alpha-b-box</v-icon>
      </v-btn>
      <v-toolbar-title>Bashoutter</v-toolbar-title>      
    </v-app-bar>

    <amplify-authenticator v-if="authState !== 'signedin'">
        <amplify-sign-in
            slot="sign-in"
            username-alias="email"
            :form-fields.prop="formFields"
        ></amplify-sign-in>
        <amplify-sign-up
            slot="sign-up"
            username-alias="email"
            :form-fields.prop="formFields"
        ></amplify-sign-up>
    </amplify-authenticator>
    <div v-if="authState === 'signedin' && user">
    <v-content>
      <amplify-greetings :username="user.username"></amplify-greetings>
      <HaikuPoster/>
      <HaikuList/>
    </v-content>
    </div>
  </v-app>
</template>

<script>
import { onAuthUIStateChange } from '@aws-amplify/ui-components'
import HaikuList from "./components/HaikuList"
import HaikuPoster from "./components/HaikuPoster"

export default {
  name: 'AuthStateApp',
  components: {
    HaikuList,
    HaikuPoster,
  },
  created() {
    this.unsubscribeAuth = onAuthUIStateChange((authState, authData) => {
      this.authState = authState;
      this.user = authData;
    })
  },
  data() {
    return {
      user: undefined,
      authState: undefined,
      unsubscribeAuth: undefined,
      formFields: [
        { type: 'email' },
        { type: 'password' },
      ]
    }
  },
  beforeDestroy() {
    this.unsubscribeAuth();
  }
}
</script>
