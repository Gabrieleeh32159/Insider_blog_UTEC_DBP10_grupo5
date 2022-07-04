<template>
  <div class="groups">
    <h2>Grupos</h2>
    <p>Estos son los grupos a los que perteneces actualmente.</p>
    <li v-if="user" v-for="group in user.groups_ids">
      <router-link to="/group/:group">{{group}}</router-link>
    </li>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import store from "@/vuex.js"
import { toDecodedMap } from '@jridgewell/gen-mapping';
import { getOuterBindingIdentifiers } from '@babel/types';

export default {
  name: "TheGroups",
  computed:{
    ...mapGetters(['user']),
  },
};

</script>

<style>
.groups {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-top: 20px;
  width: auto;
}
</style>
