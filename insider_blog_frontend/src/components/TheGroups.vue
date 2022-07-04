<template>
  <div class="groups">
    <h2>Grupos</h2>
    <p>Estos son los grupos a los que perteneces actualmente.</p>
    <div v-if="user">
      <li v-for="group in user.groups_ids" v-bind:key="group">
        <router-link
          :to="{ name: 'Groups', params: { slug: group } }"
          class="group-title"
          >{{ group }}</router-link
        >
      </li>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "TheGroups",
  data() {
    return {};
  },
  props: {},
  computed: {
    ...mapGetters(["user"]),
    ...mapGetters(["groups"]),
    groupget() {
      return this.groups.find((g) => g.group_id === this.slug);
    },
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

.group-title {
  color: #262626;
  text-decoration: none;
  font-size: 20px;
}

.group-title:hover {
  color: #4899e1;
}
</style>
