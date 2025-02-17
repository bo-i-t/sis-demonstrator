<template>
  <!--button to switch to sis page-->
  <button id="sis-button" @click="switchToSis()">
    <router-link style="color: black" to=""
      ><b-icon-folder></b-icon-folder
    ></router-link>
  </button>
</template>

<script>
import router from "../router";

export default {
  name: 'SisButton',
  methods: {
    switchToSis() {
      router.push({ name: "Sis" });
    },
  },
};
</script>

<style>
@import "../assets/styles/sisButton.css";
</style>
