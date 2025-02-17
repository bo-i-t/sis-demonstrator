<template>
  <button id="back-home-button" @click="backHome()">
    <router-link style="color: black" to=""
      ><b-icon-arrow-left></b-icon-arrow-left
    ></router-link>
  </button>
</template>

<script>
import router from "../router";

export default {
  name: 'BackHomeButton',
  methods: {
    backHome() {
      router.push("/humaine/");
    },
  },
};
</script>

<style>
@import "../assets/styles/backHomeButton.css";
</style>
