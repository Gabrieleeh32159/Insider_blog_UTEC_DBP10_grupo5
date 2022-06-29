<template>
  <TheNavigation />
  <div class="algo">
    <router-view v-bind:key="$route.path" />
    <TheGroups />
  </div>
</template>

<script>
import TheNavigation from "./components/TheNavigation.vue";
import TheGroups from "./components/TheGroups.vue";

export default {
  components: {
    TheNavigation,
    TheGroups,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.algo {
  display: flex;
  justify-content: space-between;
  margin-right: 170px;
}
</style>
