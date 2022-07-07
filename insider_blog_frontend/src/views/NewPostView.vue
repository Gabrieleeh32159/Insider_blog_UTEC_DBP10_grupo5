<template>
  <header class="site-header">
    <form @submit.prevent="handleSubmit">
      <h3>Crear Post</h3>
      <div class="content-section">
        <div class="form-group">
          <label>Title</label>
          <input
            type="title"
            class="form-control form-control-lg"
            v-model="title"
          />
        </div>

        <div class="form-group">
          <label>Content</label>
          <textarea
            class="form-control form-control-lg"
            v-model="content"
          ></textarea>
        </div>

        <div class="form-group">
          <label>Group</label>
          <select
            class="form-control form-control-lg"
            v-model="selected_group_name"
          >
            <option v-for="group in current_groups" v-bind:key="group.id">
              {{ group.group_name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <button class="btn btn-primary btn-block">Create</button>
        </div>
      </div>
    </form>
  </header>
</template>

<script>
import router from "@/router";
import store from "@/vuex";
import axios from "axios";
export default {
  name: "NewPost",
  data() {
    return {
      title: "",
      content: "",
      selected_group: "General",
      group_id: this.selected_group.id,
      current_groups: store.getters.groups,
    };
  },
  computed: {
    user() {
      return store.state.user;
    },
    search_groups() {
      return this.current_groups;
    },
  },
  methods: {
    async handleSubmit() {
      await axios
        .post("/posts", {
          title: this.title,
          content: this.content,
          user_id: store.state.user.id,
          //group_id: this.selected_group,
          group_id: store.state.groups.find(
            (g) => g.group_name == this.selected_group
          ).id,
        })
        .then(await router.push("/"));
    },
  },
};
</script>

<style>
.site-header {
  margin-top: 15px;
  padding-left: 5%;
  width: 500px;
}

.form-group {
  margin-top: 20px;
}
</style>
