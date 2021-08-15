<template>
  <v-container class="my-4 pb-10">
    <v-row justify="center" class="my-4">
      <h2 class="display-1">Submit images</h2>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-file-input
          v-model="styleImage"
          accept="image/png"
          clearable
          label="Style image"
          hint="Image must be PNG format"
          persistent-hint
          truncate-length="30"
          prepend-icon="mdi-image"
          class="pl-4"
        ></v-file-input>
      </v-col>
      <v-col cols="6">
        <v-file-input
          v-model="contentImage"
          accept="image/png"
          clearable
          label="Content image"
          hint="Image must be PNG format"
          persistent-hint
          truncate-length="30"
          prepend-icon="mdi-image"
          class="pl-4"
        ></v-file-input>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="4" class="mx-2">
        <v-slider
          v-model="styleWeight"
          label="Style weight"
          :min=50000
          :max=300000
          hint="Recommended value: 100000"
          persistent-hint
        >
          <template v-slot:append>
            <v-text-field
              v-model="styleWeight"
              class="mt-0 pt-0"
              type="number"
              style="width: 80px"
            ></v-text-field>
          </template>
        </v-slider>
      </v-col>
      <v-col cols="4" class="mx-2">
        <v-slider
          v-model="contentWeight"
          label="Content weight"
          :min=0.1
          :max=3
          :step=0.1
          hint="Recommended value: 1.0"
          persistent-hint
        >
          <template v-slot:append>
            <v-text-field
              v-model="contentWeight"
              class="mt-0 pt-0"
              type="number"
              style="width: 80px"
            ></v-text-field>
          </template>
        </v-slider>
      </v-col>
    </v-row>
    <v-row justify="center" class="mt-5">
      <v-col class="text-center">
        <v-btn class="primary"
          :disabled="!isReady"
          :loading="loading"
          @click="submit()"
          >Submit</v-btn
        >
      </v-col>
    </v-row>

    <v-dialog
      v-model="dialog"
      persistent
      width="500"
    >
      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Job successfully submitted!
        </v-card-title>

        <v-card-text>
          <div class="text-subtitle pa-12">
            The job ID is: <p class="font-weight-bold">{{ jobId }}</p>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    styleImage: undefined,
    contentImage: undefined,
    dialog: false,
    loading: false,
    styleWeight: 100000,
    contentWeight: 1,
    jobID: "",
  }),
  computed: {
    isReady: function() {
      if (this.styleImage && this.contentImage) {
        return true;
      } else {
        return false;
      }
    },
    jobId () {
      return this.$store.state.jobId
    }
  },
  methods: {
    async submit() {
      try {
        this.loading = true;
        const res = await axios.post(this.$store.state.url + "/job", {
          "style_weight": this.styleWeight,
          "content_weight": this.contentWeight,
        });

        await this.uploadFile(
          res.data.style_image_url.fields,
          this.styleImage,
          res.data.style_image_url.url
        );
        await this.uploadFile(
          res.data["content_image_url"]["fields"],
          this.contentImage,
          res.data["content_image_url"]["url"]
        );

        this.loading = false;
        this.$store.state.jobId = res.data.job_id;
        this.dialog = true;
        this.styleImage = undefined;
        this.contentImage = undefined;
      } catch (error) {
        alert(error);
      }
    },
    async uploadFile(data, file, url) {
      let formData = new FormData();
      for (const key in data) {
        if (Object.prototype.hasOwnProperty.call(data, key)) {
          formData.append(key, data[key]);
        }
      }
      formData.append("file", file);
      try {
        await axios.post(url, formData, {});
      } catch (error) {
        alert(error);
      }
    },
  },
};
</script>
