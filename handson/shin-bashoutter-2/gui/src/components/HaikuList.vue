<template>
  <v-container>
    <v-row justify="start">
      <v-col>
        <h2 class="display-2">People's Haikus</h2>
      </v-col>
      <v-col cols="2">
        <v-btn
          class="accent"
          @click="loadHaiku()"
        >
          Refresh
        </v-btn>
      </v-col>
    </v-row>
    <v-row justify="start">
      <v-col
        cols="4"
        v-for="haiku in haikus"
        v-bind:key="haiku.item_id">
        <v-card
          class="pa-2"
          outlined
        >
          <v-card-text>
            <v-row justify="space-between" class="mb-2">
              <v-col>
                <span class="caption pb-3">{{haiku.item_id}}</span>
              </v-col>
              <v-col class="text-right">
                <span class="caption pb-3">{{formatTimestamp(haiku.created_at)}}</span>
              </v-col>
            </v-row>
            <p class="display-1 text--primary">{{haiku.first}}</p>
            <p class="display-1 text--primary">{{haiku.second}}</p>
            <p class="display-1 text--primary">{{haiku.third}}</p>
            <v-row justify="space-between" align="center">
              <v-col cols="5">
                <v-btn
                  icon
                  @click="likeHaiku(haiku.item_id)">
                  <v-icon>mdi-heart</v-icon>
                </v-btn>
                <span class="ml-0 subheading">{{haiku.likes}}</span>
              </v-col>
              <v-col cols="7" class="text-right">
                <span class="title">{{haiku.username}}</span>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import moment from "moment";
import { Auth } from 'aws-amplify';

export default {
  name: "HaikuList",
  data() {
    return {
      haikus: null
    };
  },
  created: function() {
    this.loadHaiku();
  },
  methods: {
    formatTimestamp (value) {
      return moment(String(value)).format("YYYY/MM/DD hh:mm")
    },
    async loadHaiku() {
      if (!this.$store.state.url) return
      const res = await axios.get(
        this.$store.state.url + "/haiku", {
          headers: {
            Authorization: (await Auth.currentSession()).getIdToken().jwtToken,
          },
        }
      );
      this.haikus = res.data;
    },
    async likeHaiku(item_id) {
      await axios.patch(
        this.$store.state.url + "/haiku/" + item_id,
          {},
          {
            headers: {
              Authorization: (await Auth.currentSession()).getIdToken().jwtToken,
          },
        });
      await this.loadHaiku();
    }
  }
}
</script>
