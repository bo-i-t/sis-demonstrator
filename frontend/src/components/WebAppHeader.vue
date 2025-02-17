<template>
  <div class="header">
    <h1 id="headline"><b-icon-people></b-icon-people>Pflege</h1>
  </div>
</template>

<script>
export default {
  name: 'WebAppHeader',
  props: {
    title: "String",
  },
};
</script>

<style>
@import "../assets/styles/webAppHeader.css";
</style>