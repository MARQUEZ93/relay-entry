<script>
  export default {
    watch: {
      accepted(newVal) {
        this.$emit('update-accepted', newVal);
      },
    },
    props: {
      race: {
        type: Object,
        required: true,
      },
      initialAccepted: {
        type: Boolean,
        required: true,
      },
    },
    data() {
      return {
        accepted: this.initialAccepted,
      };
    },
  };
</script>

<template>
  <v-card class="mx-auto my-5 pa-3" max-width="600">
    <v-card-title>
      <h2 class="text-h5">Waiver</h2>
    </v-card-title>
    <v-card-text>
      <p class="mb-4">Please read and accept the waiver to proceed.</p>
      <v-card class="pa-3" outlined>
        <p>{{ race.event.waiver_text }}</p>
      </v-card>
      <v-checkbox
        v-model="accepted"
        label="I have read and accept the waiver"
        class="mt-3"
      ></v-checkbox>
    </v-card-text>
  </v-card>
</template>


<style scoped>
  .v-card {
    max-width: 100%;
  }
</style>
  