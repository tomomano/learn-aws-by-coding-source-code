<template>
  <v-container>
    <v-row justify="center" class="mt-5 pt-10">
      <h2 class="display-1">Check images</h2>
    </v-row>
    <v-row justify="center">
      <v-col cols="6">
        <v-text-field v-model="jobId" label="Job ID"></v-text-field>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col class="text-center">
        <v-btn class="primary"
          :disabled="!jobId"
          :loading="loading"
          @click="get()"
          >Check</v-btn
        >
      </v-col>
    </v-row>
    <v-row justify="center" class="py-2">
      <v-col class="text-center text-h5">
        Job status:
          <span class="font-weight-bold">{{ status }}</span>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <v-card v-if="styleImageUrl" outlined tile>
          <img :src="styleImageUrl" style="width:100%" />
          <v-card-subtitle>Style Image</v-card-subtitle>
        </v-card>
        <v-card v-else outlined tile>
          <img src="@/assets/Processing.png" style="width:100%" />
          <v-card-subtitle>Style Image</v-card-subtitle>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card v-if="contentImageUrl" outlined tile>
          <img :src="contentImageUrl" style="width:100%" />
          <v-card-subtitle>Content Image</v-card-subtitle>
        </v-card>
        <v-card v-else outlined tile>
          <img src="@/assets/Processing.png" style="width:100%" />
          <v-card-subtitle>Content Image</v-card-subtitle>
        </v-card>
      </v-col>
      <v-col cols="4">
        <v-card v-if="generatedImageUrl" outlined tile>
          <img :src="generatedImageUrl" style="width:100%" />
          <v-card-subtitle>Generated Image</v-card-subtitle>
        </v-card>
        <v-card v-else outlined tile>
          <img src="@/assets/Processing.png" style="width:100%" />
          <v-card-subtitle>Generated Image</v-card-subtitle>
        </v-card>
      </v-col>

    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    status: "",
    styleImageUrl: "",
    contentImageUrl: "",
    generatedImageUrl: "",
    loading: false,
  }),
  computed: {
    jobId: { 
      get () {
        return this.$store.state.jobId
      },
      set (value) {
         this.$store.commit("set_job_id", value)
      }
    }
  },
  methods: {
    async get() {
      try {
        this.loading = true;
        const res = await axios.get(`${this.$store.state.url}/job/${this.jobId}`, {});
        this.status = res.data.status;
        this.styleImageUrl = res.data.style_image_url;
        this.contentImageUrl = res.data.content_image_url;
        this.generatedImageUrl = res.data.generated_image_url;
        this.loading = false;
      } catch(error) {
        alert(error);
        this.loading = false;
      }
    },
  }
}
</script>
