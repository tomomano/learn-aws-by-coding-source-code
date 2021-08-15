<template>
  <v-app>
    <v-app-bar app color="blue" dark>
      <v-btn icon>
        <v-icon>mdi-alpha-n-box</v-icon>
      </v-btn>
      <v-toolbar-title>Neural Art Canvas</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <PostImage />
      <v-divider></v-divider>
      <CheckImage />
    </v-main>
  </v-app>
</template>

<script>
import PostImage from "./components/PostImage";
import CheckImage from "./components/CheckImage.vue";

export default {
  name: "App",
  components: {
    PostImage,
    CheckImage,
  },
  data: () => ({}),
};
</script>
