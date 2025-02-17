<template>
  <button @click="closeSession()" id="session-stop">
    <b-icon-unlock v-if="!show"></b-icon-unlock>
    <b-icon-lock-fill v-else-if="show"></b-icon-lock-fill>
  </button>
</template>

<script>
export default {
  name: 'SessionEnd',
  created() {
    this.$root.$refs.SessionEnd = this;
  },
  methods: {
    closeSession() {
      if (this.$route.path == "/humaine/") {
        this.$root.$refs.WebAppHome.popupLogout();
      } else if (this.$route.path == "/humaine/sis") {
        this.$root.$refs.Sis.popupLogout();
      }
    },
    changeIcon() {
      if (this.$session.exists()) {
        this.show = false;
      } else {
        this.show = true;
      }
    },
  },
  data() {
    return {
      show: false,
    };
  },
};
</script>

<style>
@import "../assets/styles/sessionEnd.css";
</style>
